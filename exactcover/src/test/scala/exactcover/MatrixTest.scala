package exactcover

import org.scalatest._

class MatrixTest extends FunSuite with Matchers {

  test ("basic") {
    val m = new DLXMatrix()

    m.addColumns("A", "B", "C")

    val headers = m.columnNames()
    assert(List("A", "B", "C") == headers)
  }

  test ("addrow - error") {
    val m = new DLXMatrix()

    m.addColumns("A", "B", "C")

    assertThrows[IllegalStateException] {
      m.addRow("1010")
    }

    assertThrows[IllegalArgumentException] {
      m.addRow("")
    }
  }

  ignore ("reduce and unreduce") {
    val m = new DLXMatrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

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

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

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

  test("matrix - shortest columns") {
    val m = new DLXMatrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("1111110")
    m.addRow("1111100")
    m.addRow("1111000")
    m.addRow("1110000")
    m.addRow("1100000")
    m.addRow("1000000")

    val shortest = m.shortestColumns()
    assert("G F E D C B A" === shortest.mkString(" "))
  }

  test("dlx - algorithm") {
    val m = new DLXMatrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")
    m.display()

    val dlx = new DLXAlgorithm(m)

    dlx.dlx()
  }
}
