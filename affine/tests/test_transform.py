#############################################################################
# Planar is Copyright (c) 2010 by Casey Duncan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#############################################################################

"""Transform unit tests"""

from __future__ import division
import sys
import math
import unittest
from nose.tools import assert_equal, assert_almost_equal, raises

from affine import Affine


def seq_almost_equal(t1, t2, error=0.00001):
    assert len(t1) == len(t2), "%r != %r" % (t1, t2)
    for m1, m2 in zip(t1, t2):
        assert abs(m1 - m2) <= error, "%r != %r" % (t1, t2)


class PyAffineTestCase(unittest.TestCase):

    @raises(TypeError)
    def test_zero_args(self):
        Affine()

    @raises(TypeError)
    def test_wrong_arg_type(self):
        Affine(None)

    @raises(TypeError)
    def test_args_too_few(self):
        Affine(1, 2)

    @raises(TypeError)
    def test_args_too_many(self):
        Affine(*range(10))

    @raises(TypeError)
    def test_args_members_wrong_type(self):
        Affine(0, 2, 3, None, None, "")

    def test_len(self):
        t = Affine(1, 2, 3, 4, 5, 6)
        assert_equal(len(t), 9)

    def test_slice_last_row(self):
        t = Affine(1, 2, 3, 4, 5, 6)
        assert_equal(t[-3:], (0, 0, 1))

    def test_members_are_floats(self):
        t = Affine(1, 2, 3, 4, 5, 6)
        for m in t:
            assert isinstance(m, float), repr(m)

    def test_getitem(self):
        t = Affine(1, 2, 3, 4, 5, 6)
        assert_equal(t[0], 1)
        assert_equal(t[1], 2)
        assert_equal(t[2], 3)
        assert_equal(t[3], 4)
        assert_equal(t[4], 5)
        assert_equal(t[5], 6)
        assert_equal(t[6], 0)
        assert_equal(t[7], 0)
        assert_equal(t[8], 1)
        assert_equal(t[-1], 1)

    @raises(TypeError)
    def test_getitem_wrong_type(self):
        t = Affine(1, 2, 3, 4, 5, 6)
        t['foobar']

    def test_str(self):
        assert_equal(
            str(Affine(1.111, 2.222, 3.333, -4.444, -5.555, 6.666)), 
            "| 1.11, 2.22, 3.33|\n|-4.44,-5.55, 6.67|\n| 0.00, 0.00, 1.00|")

    def test_repr(self):
        assert_equal(
            repr(Affine(1.111, 2.222, 3.456, 4.444, 5.5, 6.25)), 
            ("Affine(1.111, 2.222, 3.456,\n"
             "       4.444, 5.5, 6.25)"))

    def test_identity_constructor(self):
        ident = Affine.identity()
        assert isinstance(ident, Affine)
        assert_equal(tuple(ident), (1,0,0, 0,1,0, 0,0,1))
        assert ident.is_identity

    def test_translation_constructor(self):
        trans = Affine.translation(2, -5)
        assert isinstance(trans, Affine)
        assert_equal(tuple(trans), (1,0,2, 0,1,-5, 0,0,1))

    def test_scale_constructor(self):
        scale = Affine.scale(5)
        assert isinstance(scale, Affine)
        assert_equal(tuple(scale), (5,0,0, 0,5,0, 0,0,1))
        scale = Affine.scale(-1, 2)
        assert_equal(tuple(scale), (-1,0,0, 0,2,0, 0,0,1))
        assert_equal(tuple(Affine.scale(1)), 
            tuple(Affine.identity()))

    def test_shear_constructor(self):
        shear = Affine.shear(30)
        assert isinstance(shear, Affine)
        sx = math.tan(math.radians(30))
        seq_almost_equal(tuple(shear), (1,0,0, sx,1,0, 0,0,1))
        shear = Affine.shear(-15, 60)
        sx = math.tan(math.radians(-15))
        sy = math.tan(math.radians(60))
        seq_almost_equal(tuple(shear), (1,sy,0, sx,1,0, 0,0,1))
        shear = Affine.shear(y_angle=45)
        seq_almost_equal(tuple(shear), (1,1,0, 0,1,0, 0,0,1))

    def test_rotation_constructor(self):
        rot = Affine.rotation(60)
        assert isinstance(rot, Affine)
        r = math.radians(60)
        s, c = math.sin(r), math.cos(r)
        assert_equal(tuple(rot), (c,s,0, -s,c,0, 0,0,1))
        rot = Affine.rotation(337)
        r = math.radians(337)
        s, c = math.sin(r), math.cos(r)
        seq_almost_equal(tuple(rot), (c,s,0, -s,c,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(0)), 
            tuple(Affine.identity()))

    def test_rotation_constructor_quadrants(self):
        assert_equal(tuple(Affine.rotation(0)), (1,0,0, 0,1,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(90)), (0,1,0, -1,0,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(180)), (-1,0,0, 0,-1,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(-180)), (-1,0,0, 0,-1,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(270)), (0,-1,0, 1,0,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(-90)), (0,-1,0, 1,0,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(360)), (1,0,0, 0,1,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(450)), (0,1,0, -1,0,0, 0,0,1))
        assert_equal(tuple(Affine.rotation(-450)), (0,-1,0, 1,0,0, 0,0,1))

    def test_rotation_constructor_with_pivot(self):
        assert_equal(tuple(Affine.rotation(60)),
            tuple(Affine.rotation(60, pivot=(0,0))))
        rot = Affine.rotation(27, pivot=(2,-4))
        r = math.radians(27)
        s, c = math.sin(r), math.cos(r)
        assert_equal(tuple(rot), 
            (c,s,2 - 2*c - 4*s, -s,c,-4 - 2*s + 4*c, 0,0,1))
        assert_equal(tuple(Affine.rotation(0, (-3, 2))), 
            tuple(Affine.identity()))

    @raises(TypeError)
    def test_rotation_contructor_wrong_arg_types(self):
        Affine.rotation(1,1)

    def test_determinant(self):
        assert_equal(Affine.identity().determinant, 1)
        assert_equal(Affine.scale(2).determinant, 4)
        assert_equal(Affine.scale(0).determinant, 0)
        assert_equal(Affine.scale(5,1).determinant, 5)
        assert_equal(Affine.scale(-1,1).determinant, -1)
        assert_equal(Affine.scale(-1,0).determinant, 0)
        assert_almost_equal(Affine.rotation(77).determinant, 1)
        assert_almost_equal(Affine.translation(32, -47).determinant, 1)

    def test_is_rectilinear(self):
        assert Affine.identity().is_rectilinear
        assert Affine.scale(2.5, 6.1).is_rectilinear
        assert Affine.translation(4, -1).is_rectilinear
        assert Affine.rotation(90).is_rectilinear
        assert not Affine.shear(4, -1).is_rectilinear
        assert not Affine.rotation(-26).is_rectilinear

    def test_is_conformal(self):
        assert Affine.identity().is_conformal
        assert Affine.scale(2.5, 6.1).is_conformal
        assert Affine.translation(4, -1).is_conformal
        assert Affine.rotation(90).is_conformal
        assert Affine.rotation(-26).is_conformal
        assert not Affine.shear(4, -1).is_conformal

    def test_is_orthonormal(self):
        assert Affine.identity().is_orthonormal
        assert Affine.translation(4, -1).is_orthonormal
        assert Affine.rotation(90).is_orthonormal
        assert Affine.rotation(-26).is_orthonormal
        assert not Affine.scale(2.5, 6.1).is_orthonormal
        assert not Affine.scale(.5, 2).is_orthonormal
        assert not Affine.shear(4, -1).is_orthonormal

    def test_is_degenerate(self):
        from affine import EPSILON
        assert not Affine.identity().is_degenerate
        assert not Affine.translation(2, -1).is_degenerate
        assert not Affine.shear(0, -22.5).is_degenerate
        assert not Affine.rotation(88.7).is_degenerate
        assert not Affine.scale(0.5).is_degenerate
        assert Affine.scale(0).is_degenerate
        assert Affine.scale(-10, 0).is_degenerate
        assert Affine.scale(0, 300).is_degenerate
        assert Affine.scale(0).is_degenerate
        assert Affine.scale(0).is_degenerate
        assert Affine.scale(EPSILON).is_degenerate

    def test_column_vectors(self):
        import affine
        a, b, c = Affine(2, 3, 4, 5, 6, 7).column_vectors
        assert isinstance(a, tuple)
        assert isinstance(b, tuple)
        assert isinstance(c, tuple)
        assert_equal(a, (2, 5))
        assert_equal(b, (3, 6))
        assert_equal(c, (4, 7))

    def test_almost_equals(self):
        from affine import EPSILON
        assert EPSILON != 0, EPSILON
        E = EPSILON * 0.5
        t = Affine(1.0, E, 0, -E, 1.0+E, E)
        assert t.almost_equals(Affine.identity())
        assert Affine.identity().almost_equals(t)
        assert t.almost_equals(t)
        t = Affine(1.0, 0, 0, -EPSILON, 1.0, 0)
        assert not t.almost_equals(Affine.identity())
        assert not Affine.identity().almost_equals(t)
        assert t.almost_equals(t)

    def test_equality(self):
        t1 = Affine(1, 2, 3, 4, 5, 6)
        t2 = Affine(6, 5, 4, 3, 2, 1)
        t3 = Affine(1, 2, 3, 4, 5, 6)
        assert t1 == t3
        assert not t1 == t2
        assert t2 == t2
        assert not t1 != t3
        assert not t2 != t2
        assert t1 != t2
        assert not t1 == 1
        assert t1 != 1

    @raises(TypeError)
    def test_gt(self):
        Affine(1,2,3,4,5,6) > Affine(6,5,4,3,2,1)

    @raises(TypeError)
    def test_lt(self):
        Affine(1,2,3,4,5,6) < Affine(6,5,4,3,2,1)

    @raises(TypeError)
    def test_add(self):
        Affine(1,2,3,4,5,6) + Affine(6,5,4,3,2,1)
        
    @raises(TypeError)
    def test_sub(self):
        Affine(1,2,3,4,5,6) - Affine(6,5,4,3,2,1)

    def test_mul_by_identity(self):
        t = Affine(1,2,3,4,5,6)
        assert_equal(tuple(t * Affine.identity()), tuple(t))

    def test_mul_transform(self):
        t = Affine.rotation(5) * Affine.rotation(29)
        assert isinstance(t, Affine)
        seq_almost_equal(t, Affine.rotation(34))
        t = Affine.scale(3, 5) * Affine.scale(2)
        seq_almost_equal(t, Affine.scale(6, 10))

    def test_itransform(self):
        pts = [(4,1), (-1,0), (3,2)]
        r = Affine.scale(-2).itransform(pts)
        assert r is None, r
        assert_equal(pts, [(-8, -2), (2,0), (-6,-4)])

    @raises(TypeError)
    def test_mul_wrong_type(self):
        Affine(1,2,3,4,5,6) * None

    @raises(TypeError)
    def test_mul_sequence_wrong_member_types(self):
        class NotPtSeq:
            @classmethod
            def from_points(cls, points):
                list(points)
            def __iter__(self):
                yield 0
        Affine(1,2,3,4,5,6) * NotPtSeq()
        
    def test_imul_transform(self):
        t = Affine.translation(3, 5)
        t *= Affine.translation(-2, 3.5)
        assert isinstance(t, Affine)
        seq_almost_equal(t, Affine.translation(1, 8.5))

    def test_inverse(self):
        seq_almost_equal(~Affine.identity(), Affine.identity())
        seq_almost_equal(
            ~Affine.translation(2, -3), Affine.translation(-2, 3))
        seq_almost_equal(
            ~Affine.rotation(-33.3), Affine.rotation(33.3))
        t = Affine(1,2,3,4,5,6)
        seq_almost_equal(~t * t,  Affine.identity())
    
    def test_cant_invert_degenerate(self):
        from affine import TransformNotInvertibleError
        t = Affine.scale(0)
        self.assertRaises(TransformNotInvertibleError, lambda: ~t)

    def test_set_epsilon(self):
        import affine

        old_epsilon = affine.EPSILON
        old_epsilon2 = affine.EPSILON2

        try:
            affine.set_epsilon(123)
            assert_equal(123, affine.EPSILON)
            assert_equal(123*123, affine.EPSILON2)
        finally:
            affine.set_epsilon(old_epsilon)
            

        


def test_gdal():
    t = Affine.from_gdal(-237481.5, 425.0, 0.0, 237536.4, 0.0, -425.0)
    assert t.c == t.xoff == -237481.5
    assert t.a == 425.0
    assert t.b == 0.0
    assert t.f == t.yoff ==  237536.4
    assert t.d == 0.0
    assert t.e == -425.0
    assert tuple(t) == (425.0, 0.0, -237481.5, 0.0, -425.0, 237536.4, 0, 0, 1.0)
    assert t.to_gdal() == (-237481.5, 425.0, 0.0, 237536.4, 0.0, -425.0)


if __name__ == '__main__':
    unittest.main()


# vim: ai ts=4 sts=4 et sw=4 tw=78

