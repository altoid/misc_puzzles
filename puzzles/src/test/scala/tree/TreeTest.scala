package tree

import org.scalatest.FunSuite
import roman.RomanNumeral

class TreeTest extends FunSuite {
  test("basics") {
    val t = new Tree[Int]()

    assert(0 === t.size())
    assert(0 === t.height())
  }

  test("singleton") {
    val t = new Tree[Int]()

    t.addValue(1)

    assert(1 === t.size())
    assert(1 === t.height())
  }

  test("nontrivial") {
    val t = new Tree[Int]()

    t.addValues(8, 3, 9, 1, 5, 12, 4, 11)
    assert(8 === t.size())
    assert(4 === t.height())
    assert(t.contains(12))
    assert(!t.contains(66))

    t.addValues(8, 8, 8, 8, 8)
    assert(8 === t.size())
    assert(4 === t.height())

    assert(1 === t.min())
    assert(12 === t.max())
  }
}
