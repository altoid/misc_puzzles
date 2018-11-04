package tree

import org.scalatest.FunSuite
import roman.RomanNumeral

class TreeTest extends FunSuite {
  test("construction") {
    val t: Tree[Int] = Node(1, Node(2, Empty, Leaf(9)), Node(3, Leaf(4), Leaf(5)))
  }
}
