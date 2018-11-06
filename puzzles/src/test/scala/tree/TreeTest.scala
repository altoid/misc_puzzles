package tree

import org.scalatest.FunSuite
import org.scalatest.OptionValues
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

  test("many inserts") {
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

  test("successor") {
    val t = new Tree[Int]()

    t.addValues(8, 3, 9, 1, 5, 12, 4, 11)

    assert(t.successor(9) == Some(11))
    assert(t.successor(1) == None)
    assert(t.successor(12) == None)
    assert(t.successor(8) == Some(9))
  }
}
