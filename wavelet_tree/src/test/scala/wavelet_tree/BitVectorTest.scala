package wavelet_tree

import org.scalatest.FunSuite

class BitVectorTest extends FunSuite {
  test("width") {
    assert(BitVector.width(19) == 5)
    assert(BitVector.width(0) == 0)
    assert(BitVector.width(16) == 5)
    assert(BitVector.width(15) == 4)
  }

  test("construction") {
    val bv = new BitVector(Array(31, 0, 16, 15), 0)
    assert(bv.width == 5)
    assert(bv.mask == 16)
    assert(bv.bits === Array(1,0,1,0))
  }

  test("construction II") {
    val bv = new BitVector(Array(1,7,2,4,6,1,3,0,5), 0)
    assert(bv.bits === Array(0,1,0,1,1,0,0,0,1))
    assert(bv.zeroesBefore === Array(0,1,1,2,2,2,3,4,5))
    assert(bv.onesBefore === Array(0,0,1,1,2,3,3,3,3))
  }

  test("range counting") {
    val bv = new BitVector(Array(1,7,2,4,6,1,3,0,5), 0)

    assert(bv.zeroesInRange(3, 7) == 3)
    assert(bv.onesInRange(3, 7) == 2)

    assert(bv.zeroesInRange(4, 8) == 3)
    assert(bv.onesInRange(4, 8) == 2)

    assert(bv.zeroesInRange(0, 8) == 5)
    assert(bv.onesInRange(0, 8) == 4)

  }
}
