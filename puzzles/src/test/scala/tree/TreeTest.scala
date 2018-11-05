package tree

import org.scalatest.FunSuite
import roman.RomanNumeral

class TreeTest extends FunSuite {
  test("basics") {
    val t = new Tree[Int]()

    assert(0 == t.size())
    assert(0 == t.height())
  }

  test("singleton") {
    val t = new Tree[Int]()

    t.addValue(1)

    assert(1 == t.size())
    assert(1 == t.height())
  }
}
