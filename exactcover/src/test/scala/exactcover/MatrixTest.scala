package exactcover

import org.scalatest.FunSuite

import exactcover.Matrix

class MatrixTest extends FunSuite {

  test ("basic") {
    val m = new Matrix()

    m.addColumns("A", "B", "C")

    val headers = m.columnNames()
    println(headers)
  }
}
