"""Check the paths and entry points most likely to break during a repo move.

Run with: python -m unittest discover -s tests
Simulation/model checks require the project dependencies, but not h5py or a GPU.
"""
import importlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
import torch

from robot_learning.cli import load_config, main
from robot_learning.utils.paths import REPO_ROOT, resolve_repo_path


class StructureSmokeTests(unittest.TestCase):
    def test_paths_and_legacy_imports(self):
        from util.paths import REPO_ROOT as legacy_root
        from robot_learning.experts.bin_sort import BinSortExpert
        from robot_learning.hw1_oracle_policy import HW1BinSortExpert

        self.assertEqual(REPO_ROOT, Path(__file__).resolve().parents[1])
        self.assertEqual(legacy_root, REPO_ROOT)
        self.assertIs(BinSortExpert, HW1BinSortExpert)
        self.assertEqual(resolve_repo_path('outputs/example.h5'), REPO_ROOT / 'outputs/example.h5')
        self.assertEqual(load_config(), load_config(REPO_ROOT / 'robot_learning/environment/default.yaml'))

    def test_workflow_imports(self):
        for name in ['collect_sim_data', 'train_bc', 'eval_policy', 'diagnose_conditioning', 'plot_training']:
            importlib.import_module('robot_learning.scripts.' + name)

    def test_legacy_and_explicit_collection_dispatch(self):
        for args in [['collect', '--episodes', '2', '--seed', '0'], ['--episodes', '2']]:
            with patch.object(sys, 'argv', ['robot-learning', *args]):
                with patch('robot_learning.scripts.collect_sim_data.collect_sim_data') as collect:
                    main()
                    self.assertEqual(collect.call_args.kwargs['episodes'], 2)
                    self.assertEqual(collect.call_args.kwargs['output_path'], resolve_repo_path(load_config()['data']['dataset_path']))

    def test_scene_reset_and_step(self):
        from robot_learning.environment import VLAIRB120Env

        with VLAIRB120Env(seed=0) as env:
            observation, _ = env.reset(seed=0)
            self.assertEqual(observation.shape, (24,))
            self.assertTrue(np.isfinite(observation).all())
            observation, _, _ = env.step(env.data.qpos[:6].copy())
            self.assertTrue(np.isfinite(observation).all())

    def test_policy_shapes_and_state_dicts(self):
        from robot_learning.models.policy import StateOnlyBCPolicy, GoalConditionedBCPolicy, TinyVLAPolicy

        state = torch.zeros(2, 24)
        for policy_type in [StateOnlyBCPolicy, GoalConditionedBCPolicy, TinyVLAPolicy]:
            policy = policy_type()
            restored = policy_type()
            restored.load_state_dict(policy.state_dict(), strict=True)
            if policy_type is StateOnlyBCPolicy:
                action = restored(state)
            elif policy_type is GoalConditionedBCPolicy:
                action = restored(state, torch.zeros(2, 5))
            else:
                action = restored(torch.zeros(2, 3, 128, 128), state, ['sort the cube'] * 2)
            self.assertEqual(action.shape, (2, 6))
            self.assertTrue(torch.isfinite(action).all())
