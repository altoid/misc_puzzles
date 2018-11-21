package sudoku

import exactcover._

import scala.collection.mutable.ArrayBuffer

class Sudoku(var size: Int) {
  assert(size == 4 || size == 9)

  /*
          columns

          0 1 2 .. 8

        0     0  1  2
        1
   rows :     3  4  5     regions
        :
        8     6  7  8

  */

  def rowFor(r: Int, c: Int) = r
  def columnFor(r: Int, c: Int) = c
  def regionFor(r: Int, c: Int): Int = {
    val size_sqrt = math.sqrt(size).toInt

    c / size_sqrt + (r / size_sqrt) * size_sqrt
  }

  def cellFor(r: Int, c: Int): Int = {
    c + r * size
  }

  def cellToRow(r: Int, c: Int, value: Int): String = {
    var columnPart = ArrayBuffer.fill(size * size)("0")
    val column = columnFor(r, c)
    columnPart(column * size + (value - 1)) = "1"

    var rowPart = ArrayBuffer.fill(size * size)("0")
    val row = rowFor(r, c)
    rowPart(row * size + (value - 1)) = "1"

    var regionPart = ArrayBuffer.fill(size * size)("0")
    val region = regionFor(r, c)
    regionPart(region * size + (value - 1)) = "1"

    var cellPart = ArrayBuffer.fill(size * size)("0")
    val cell = cellFor(r, c)
    cellPart(cell) = "1"

    (cellPart ++ rowPart ++ columnPart ++ regionPart).mkString
  }

  def rowToCell(row: String): Tuple3[Int, Int, Int] = {
    val cellPart = row.substring(0, size * size)
    val rowPart = row.substring(size * size, 2 * size * size)

    val cellindex = cellPart.indexOf('1')
    val rowindex = rowPart.indexOf('1')

    val value = rowindex % size + 1

    val r = rowindex / size
    val c = rowindex - r * size

    (r, c, value)
  }
}

object Sudoku {
  def main(args: Array[String]): Unit = {
    val sz = 4
    val sdk = new Sudoku(sz)

    for (r <- 0 until sz) {
      for (c <- 0 until sz) {
        for (v <- 1 to sz) {
          val row = sdk.cellToRow(r, c, v)
          val (rw, cl, vl) = sdk.rowToCell(row)
          println(row + s" - row $rw, col $cl, val $vl")
        }
      }
    }
  }
}
