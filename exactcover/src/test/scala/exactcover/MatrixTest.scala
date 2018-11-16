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

  ignore ("reduce and unreduce") {
    val m = new Matrix()

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
      case Some(ch) => {
        m.cover(ch)

        val b = ch.d match {
          case x: Bit => x
          case _ => throw new IllegalArgumentException
        }

        m.reduce_by_row(b)
        println("reducing")
        m.display()

        println("unreducing")
        m.unreduce_by_row(b)
        m.display()

        println("uncovering")
        m.uncover(ch)
        m.display()
      }
    }

  }

  ignore ("cover and uncover") {
    val m = new Matrix()

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

  test ("dlx - algorithm") {
    val m = new Matrix()

    m.addColumns("A", "B", "C", "D", "E", "F", "G")

    m.addRow("0010110")
    m.addRow("1001001")
    m.addRow("0110010")
    m.addRow("1001000")
    m.addRow("0100001")
    m.addRow("0001101")

    val dlx = new DLXAlgorithm(m)

    dlx.dlx()
  }
}
