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

  test("contains") {
    val t = new Tree[Int]()

    assert(!t.contains(1))

    t.addValues(1)
    assert(t.contains(1))
    assert(!t.contains(2))
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

  test("preorder") {
    val t = new Tree[Int]()

    assert(List[Int]() == t.preorder())

    t.addValue(8)
    assert(List(8) == t.preorder())

    t.addValues(3,9,1,5,12,4,7,11,13,10)
    assert(List(8,3,1,5,4,7,9,12,11,10,13) == t.preorder())
  }

  ignore("delete from empty tree") {
    val t = new Tree[Int]()

    t.deleteValue(9)

    assert(0 === t.size())
    assert(0 === t.height())
    assert(!t.contains(9))
  }


  ignore("delete from single-node tree") {
    val t = new Tree[Int]()

    t.addValue(12)

    t.deleteValue(9)
    assert(!t.contains(9))

    t.deleteValue(12)
    assert(0 === t.size())
    assert(0 === t.height())
  }


  //       12      delete 11      12
  //      /        -------->
  //     11
  // 

  test ("case 3") {
    val t = new Tree[Int]()

    t.addValues(12, 11)

//    t.deleteValue(100)

    t.deleteValue(11)

    assert(1 === t.size())
    assert(1 === t.height())

    val n = t.locus(12)
    assert(n.children(0) === None)
    assert(n.children(1) === None)
    assert(n.parent === None)

    assert(List(12) === t.preorder())
  }

  // 
  //       12      delete 12      11
  //      /        -------->
  //     11
  //

  test("case 4") {
    val t = new Tree[Int]()

    t.addValues(12, 11)

    t.deleteValue(100)

    t.deleteValue(12)

    assert(1 === t.size())
    assert(1 === t.height())

    val n = t.locus(12)

    assert(None === n)

    assert(List(11) === t.preorder())
  }

  // 
  //       12      delete 12      13
  //      /  \     -------->     /
  //     11  13                 11

  test("case 5") {
    val t = new Tree[Int]()

    t.addValues(12, 11, 13)

    t.deleteValue(100)

    t.deleteValue(12)

    assert(2 === t.size())
    assert(2 === t.height())

    val n = t.locus(12)

    assert(None === n)

    assert(List(13, 11) === t.preorder())
  }
}