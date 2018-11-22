package sudoku

import exactcover._

import scala.collection.mutable.ArrayBuffer
import scala.io.Source

class Sudoku(val size: Int) {
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

  val matrix = new DLXMatrix()

  private val fileToRead = size match {
    case 4 => "sudoku4_data.txt"
    case 9 => "sudoku9_data.txt"
    case _ => throw new IllegalArgumentException
  }

  private val lines: Iterator[String] = Source.fromResource(fileToRead).getLines()

  private val headers = lines.next()
  // headers.foreach(c => matrix.addColumn(c.toString))
  (0 until 4 * size * size) foreach (i => matrix.addColumn(i.toString))

  while (lines.hasNext) {
    val row = lines.next()
    matrix.addRow(row)
  }

  private def rowFor(r: Int, c: Int) = r
  private def columnFor(r: Int, c: Int) = c
  private def regionFor(r: Int, c: Int): Int = {
    val size_sqrt = math.sqrt(size).toInt

    c / size_sqrt + (r / size_sqrt) * size_sqrt
  }

  private def cellFor(r: Int, c: Int): Int = {
    c + r * size
  }

  def cellToRow(r: Int, c: Int, value: Int): String = {
    val columnPart = ArrayBuffer.fill(size * size)("0")
    val column = columnFor(r, c)
    columnPart(column * size + (value - 1)) = "1"

    val rowPart = ArrayBuffer.fill(size * size)("0")
    val row = rowFor(r, c)
    rowPart(row * size + (value - 1)) = "1"

    val regionPart = ArrayBuffer.fill(size * size)("0")
    val region = regionFor(r, c)
    regionPart(region * size + (value - 1)) = "1"

    val cellPart = ArrayBuffer.fill(size * size)("0")
    val cell = cellFor(r, c)
    cellPart(cell) = "1"

    (cellPart ++ rowPart ++ columnPart ++ regionPart).mkString
  }

  def rowToCell(row: String): Tuple3[Int, Int, Int] = {
    val columnPart = row.substring(2 * size * size, 3 * size * size)
    val rowPart = row.substring(size * size, 2 * size * size)

    val columnindex = columnPart.indexOf('1')
    val rowindex = rowPart.indexOf('1')

    val value = rowindex % size + 1

    val r = rowindex / size
    val c = columnindex / size

    (r, c, value)
  }
}

object Sudoku {
  def main(args: Array[String]): Unit = {
    if (args.length < 1) {
      println("no args")
      return
    }

    val filename = args(0)

    val linesItr = Source.fromFile(filename).getLines()

    val size = linesItr.next().toInt
    var tableau = ArrayBuffer[Array[Int]]()

    while (linesItr.hasNext) {
      val row = linesItr.next().split(" ").map(_.toInt)
      tableau = tableau :+ row
      row.foreach(n => print(n + " "))
      println
    }

    val sdk = new Sudoku(size)

    var seeds = ArrayBuffer[String]()
    for (r <- 0 until size) {
      for (c <- 0 until size) {
        val v = tableau(r)(c)
        if (v != 0) {
          val seed = sdk.cellToRow(r, c, v)
          seeds = seeds :+ seed
        }
      }
    }

    val dlx = new DLXAlgorithm(sdk.matrix)

    dlx.dlx(DLXMatrix.shortestColumns, Some(seeds))

    val solved = Array.ofDim[Int](size, size)
    val solution = dlx.solutions.toVector(0)
    solution.foreach(rh => {
      val (r, c, value) = sdk.rowToCell(rh.bits)
      solved(r)(c) = value
    })

    println("============================ solution")
    for (r <- 0 until size) {
      for (c <- 0 until size) {
        print(solved(r)(c) + " ")
      }
      println
    }

    println("nodes:  " + dlx.nodes)
    println("leaves:  " + dlx.leaves)
  }
}
