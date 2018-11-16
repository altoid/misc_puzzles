package exactcover

import org.scalatest._

import exactcover.Matrix

class MatrixTest extends FunSuite with Matchers {

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

        // covering is idempotent
        m.cover(ch)
        m.display()

        m.uncover(ch)
        m.display()
      }
    }
  }

  test ("dlx - shortest") {
    val m = new Matrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val dlx = new DLXAlgorithm(m)

    var shortest = dlx.shortest() match {
      case Some(columnHeader: ColumnHeader) => columnHeader
      case None => throw new IllegalArgumentException
    }

    assert(shortest.name === "A")

    var och = dlx.matrix.findColumn("A")

    och match {
      case Some(ch) => dlx.matrix.cover(ch)
      case None => throw new IllegalArgumentException
    }

    shortest = dlx.shortest() match {
      case Some(columnHeader: ColumnHeader) => columnHeader
      case None => throw new IllegalArgumentException
    }

    assert(shortest.name === "D")
    assert(shortest.count === 1)
  }
}
