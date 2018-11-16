package exactcover

import org.scalatest.FunSuite

import exactcover.Matrix

class MatrixTest extends FunSuite {

  test ("basic") {
    val m = new Matrix()

    m.addColumns("A", "B", "C")

    val headers = m.columnNames()
    assert(List("A", "B", "C") == headers)
  }

  test ("addrow - error") {
    val m = new Matrix()

    m.addColumns("A", "B", "C")

    assertThrows[IllegalStateException] {
      m.addRow("1010")
    }

    assertThrows[IllegalArgumentException] {
      m.addRow("")
    }
  }

  test ("cover and uncover") {
    val m = new Matrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("0010110")
//    m.addRow("0000000")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")
    m.display()

    val ch = m.findColumn("A")
    ch match {
      case None => throw new NoSuchElementException
      case Some(ch) => {
        m.cover(ch)
        m.display()

        m.uncover(ch)
        m.display()
      }
    }
  }
}
