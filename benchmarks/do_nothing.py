# Copyright (c) 2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of LightSim2grid, LightSim2grid a implements a c++ backend targeting the Grid2Op platform.

from grid2op import make
from grid2op.Agent import DoNothingAgent
from grid2op.Parameters import Parameters
from lightsim2grid.LightSimBackend import LightSimBackend
from utils_benchmark import print_res, run_env

MAX_TS = 1000
ENV_NAME = "rte_case14_realistic"


def main(max_ts, ENV_NAME):
    backend = LightSimBackend()
    param = Parameters()
    param.init_from_dict({"NO_OVERFLOW_DISCONNECTION": True})

    env_klu = make(ENV_NAME, backend=backend, param=param, test=True)
    agent = DoNothingAgent(action_space=env_klu.action_space)
    nb_ts_klu, time_klu, aor_klu, gen_p_klu, gen_q_klu = run_env(env_klu, max_ts, agent)

    env_pp = make(ENV_NAME, param=param, test=True)
    agent = DoNothingAgent(action_space=env_pp.action_space)
    nb_ts_pp, time_pp, aor_pp, gen_p_pp, gen_q_pp = run_env(env_pp, max_ts, agent)

    print_res(env_klu, env_pp,
              nb_ts_klu, nb_ts_pp,
              time_klu, time_pp,
              aor_klu, aor_pp,
              gen_p_klu, gen_p_pp,
              gen_q_klu, gen_q_pp
              )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Benchmark pyKLU and Pandapower Backend for a "do nothing" agent')
    parser.add_argument('--name', default=ENV_NAME, type=str,
                        help='Environment name to be used for the benchmark.')
    parser.add_argument('--number', type=int, default=MAX_TS,
                        help='Maximum number of time steps for which the benchamark will be run.')

    args = parser.parse_args()

    max_ts = int(args.number)
    name = str(args.name)
    main(max_ts, name)
