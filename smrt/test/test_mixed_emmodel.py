# coding: utf-8

import numpy as np
from nose.tools import ok_

# local import
from smrt import make_snowpack, make_model, sensor_list


def test_mixed_emmodel():
    # prepare inputs
    l = 2

    nl = l//2  # // Forces integer division
    thickness = np.array([0.1, 0.1]*nl)
    thickness[-1] = 100  # last one is semi-infinit
    radius = np.array([2e-4]*l)
    temperature = np.array([250.0, 250.0]*nl)
    density = [200, 400]*nl
    stickiness = [0.1, 0.1]*nl
    emmodel = ["dmrt_qcacp_shortrange", "iba"]*nl

    # create the snowpack
    snowpack = make_snowpack(thickness,
                             "sticky_hard_spheres",
                             density=density,
                             temperature=temperature,
                             radius=radius,
                             stickiness=stickiness)

    # create the EM Model
    m = make_model(emmodel, "dort")

    # create the sensor
    radiometer = sensor_list.amsre('37V')

    # run the model
    res = m.run(radiometer, snowpack)

    print(res.TbV(), res.TbH())

    #ok_((res.TbV() - 203.84730126016882) < 1e-4)
    #ok_((res.TbH() - 189.53130277932084) < 1e-4)



    #ok_((res.TbV() - 203.8473395866384) < 1e-4)
    #ok_((res.TbH() - 189.53346053779396) < 1e-4)

    ok_((res.TbV() - 204.62367102418355) < 1e-4)
    ok_((res.TbH() - 190.38540104288276) < 1e-4)
