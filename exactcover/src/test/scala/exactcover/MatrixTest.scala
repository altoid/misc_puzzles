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

  test ("display") {
    val m = new Matrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("0010110")
    m.addRow("0000000")
    m.display()
  }
}
