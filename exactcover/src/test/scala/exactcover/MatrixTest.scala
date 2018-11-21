package exactcover

import org.scalatest._

import scala.collection.mutable.ArrayBuffer

class MatrixTest extends FunSuite with Matchers {

  test ("basic") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C"))

    val headers = m.columnNames()
    assert(List("A", "B", "C") == headers)
  }

  test ("addrow - error") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C"))

    assertThrows[IllegalStateException] {
      m.addRow("1010")
    }

    assertThrows[IllegalArgumentException] {
      m.addRow("")
    }
  }

  ignore ("reduce and unreduce") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val ch = m.findColumn("A")
    ch match {
      case None => throw new NoSuchElementException
      case Some(x) => {
        m.cover(x)

        val b = x.d match {
          case y: Bit => y
          case _ => throw new IllegalArgumentException
        }

        m.reduce_by_row(b)
        println("reducing")
        m.display()

        println("unreducing")
        m.unreduce_by_row(b)
        m.display()

        println("uncovering")
        m.uncover(x)
        m.display()
      }
    }

  }

  ignore ("cover and uncover") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")
    m.display()

    val ch = m.findColumn("A")
    ch match {
      case None => throw new NoSuchElementException
      case Some(x) => {
        m.cover(x)
        m.display()

        // covering is idempotent
        m.cover(x)
        m.display()

        m.uncover(x)
        m.display()
      }
    }
  }

  ignore("matrix - shortest columns") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("1111110")
    m.addRow("1111100")
    m.addRow("1111000")
    m.addRow("1110000")
    m.addRow("1100000")
    m.addRow("1000000")

    val shortest = DLXMatrix.shortestColumns(m)
    assert("G F E D C B A" === shortest.mkString(" "))
  }

  ignore("dlx - algorithm") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val dlx = new DLXAlgorithm(m)

    dlx.dlx(DLXMatrix.shortestColumns)

    assert(dlx.solutions.size === 1)
    assert(dlx.solutions.toVector(0).map(_.index) === Vector(0, 3, 4))

    for (s <- dlx.solutions) {
      dlx.matrix.display(Some(s))
    }

    println(s"leaves = ${dlx.leaves}")
    println(s"nodes = ${dlx.nodes}")
  }

  test("dlx - leftmost vs. shortest") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G", "H"))

    m.addRow("10010110")
    m.addRow("11001001")
    m.addRow("10110010")
    m.addRow("01001000")
    m.addRow("00100001")
    m.addRow("10001101")

    val dlx = new DLXAlgorithm(m)

    dlx.dlx(DLXMatrix.leftMost)

    assert(dlx.solutions.size === 1)
    assert(dlx.solutions.toVector(0).map(_.index) === Vector(0, 3, 4))

    println("leftmost:")
    println(s"leaves = ${dlx.leaves}")
    println(s"nodes = ${dlx.nodes}")

    dlx.dlx(DLXMatrix.shortestColumns)

    assert(dlx.solutions.size === 1)
    assert(dlx.solutions.toVector(0).map(_.index) === Vector(0, 3, 4))

    println("shortestColumns:")
    println(s"leaves = ${dlx.leaves}")
    println(s"nodes = ${dlx.nodes}")
  }

  test("dlx - no solution") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G", "H", "I"))

    m.addRow("100101100")
    m.addRow("110010010")
    m.addRow("101100100")
    m.addRow("010010000")
    m.addRow("001000010")
    m.addRow("100011010")

    val dlx = new DLXAlgorithm(m)

    dlx.dlx(DLXMatrix.shortestColumns)

    assert(dlx.solutions.size === 0)

    println(s"leaves = ${dlx.leaves}")
    println(s"nodes = ${dlx.nodes}")
  }

  test("dlx - seed - solution") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val dlx = new DLXAlgorithm(m)

    val seed = Vector("0010110")
    dlx.dlx(DLXMatrix.shortestColumns, Some(seed))

    assert(dlx.solutions.size === 1)
    assert(dlx.solutions.toVector(0).map(_.index) === Vector(0, 3, 4))
  }

  test("dlx - seed - no solution") {
    val m = new DLXMatrix()

    m.addColumns(List("A", "B", "C", "D", "E", "F", "G"))

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val dlx = new DLXAlgorithm(m)

    val seed = Vector("1001001")
    dlx.dlx(DLXMatrix.shortestColumns, Some(seed))

    assert(dlx.solutions.size === 0)
  }
}
