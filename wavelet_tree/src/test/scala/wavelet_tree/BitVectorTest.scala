package wavelet_tree

import org.scalatest.FunSuite

class BitVectorTest extends FunSuite {
  test("width") {
    assert(BitVector.width(19) == 5)
    assert(BitVector.width(0) == 0)
    assert(BitVector.width(16) == 5)
    assert(BitVector.width(15) == 4)
  }

  test("seq uniques") {
    assert(Array(1,2,3,4,5).groupBy(identity).size > 1)
    assert(Array(1).groupBy(identity).size == 1)
    assert(Array(1,1,1,1,1,1).groupBy(identity).size == 1)
  }

  test("construction") {
    val bv = new BitVector(Array(31, 0, 16, 15))
    assert(bv.width == 5)
    assert(bv.mask == 16)
    assert(bv.bits === Array(1,0,1,0))
  }

  test("construction II") {
    val bv = new BitVector(Array(1,7,2,4,6,1,3,0,5))
    assert(bv.bits === Array(0,1,0,1,1,0,0,0,1))
    assert(bv.zeroesBefore === Array(0,1,1,2,2,2,3,4,5))
    assert(bv.onesBefore === Array(0,0,1,1,2,3,3,3,3))
  }

  test("range counting") {
    val bv = new BitVector(Array(1,7,2,4,6,1,3,0,5))

    assert(bv.zeroesInRange(3, 7) == 3)
    assert(bv.onesInRange(3, 7) == 2)

    assert(bv.zeroesInRange(4, 8) == 3)
    assert(bv.onesInRange(4, 8) == 2)

    assert(bv.zeroesInRange(0, 8) == 5)
    assert(bv.onesInRange(0, 8) == 4)
  }

  test("partition") {
    val a: Array[Int] = Array(1,7,2,4,6,1,3,0,5)

    var bv = new BitVector(a)

    val (parta, partb) = bv.partition()

    assert(parta === Array(1,2,1,3,0))
    assert(partb === Array(7,4,6,5))

    // partition preserves the relative order of the elements in each part.

    bv = new BitVector(parta)
    val (part2a, part2b) = bv.partition()
    assert(part2a === Array(1,1,0))
    assert(part2b === Array(2, 3))
  }

  test("WT construction") {
    val wt = new WaveletTree(Array(1,7,2,4,6,1,3,0,5))
    wt.dump()
  }
}