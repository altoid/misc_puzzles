package boggle

import scala.io.Source
import scala.util.Random
import scala.collection.mutable.ListBuffer

class Cell(l: Char) {
    val letter = l
    var visited: Boolean = false

  override def toString: String = letter.toString
}

object Cell {
  def apply(letter: Char): Cell = new Cell(letter)

  implicit def toCell(letter: Char) = Cell(letter)
}

object Board {
  val alphabet = "abcdefghijklmnoprstuvwxyz".toCharArray // q is omitted
  val size = 4
  val displayColumns = 6
}

class Board {

  private val tableau: Array[Cell] = Array.fill[Cell](Board.size * Board.size)(Board.alphabet(Random.nextInt(Board.alphabet.length)))

  val all_words: List[String] = Source.fromResource("all.txt").getLines().toList
  var results: List[String] = List[String]()

  private var current_path = ListBuffer[Char]()

  def display(): Unit = {
    for (i <- 0 until Board.size) {
      for (j <- 0 until Board.size) {
        print(tableau(i * Board.size + j) + " ")
      }
      println
    }
  }

  def words_matching_prefix(prefix: String, current_matches: Seq[String]) = {
    current_matches.filter(x => x.startsWith(prefix))
  }

  def visit(r: Int, c: Int, current_matches: Seq[String]): Unit = {
    if (r < 0) return
    if (r >= Board.size) return
    if (c < 0) return
    if (c >= Board.size) return

    val cell: Cell = tableau(r * Board.size + c)
    if (cell.visited) return

    cell.visited = true

    current_path += cell.letter

    val prefix = current_path.mkString

    val new_matches = words_matching_prefix(prefix, current_matches)

    if (new_matches.nonEmpty) {
      val w = new_matches.filter(x => x == prefix)
      if (w.nonEmpty) {
        results = results :+ w.head
      }

      for {
        dr <- -1 until 2
        dc <- -1 until 2 if dc != 0 || dr != 0
      } visit(r + dr, c + dc, new_matches)
    }
    cell.visited = false
    current_path = current_path.dropRight(1)
  }

  def traverse_from(r: Int, c: Int): Unit = {
    visit(r, c, all_words)
  }

  def play(): Unit = {
    display()

    for (r <- 0 until Board.size; c <- 0 until Board.size) {
        traverse_from(r, c)
    }

    val nwords = results.length
    println(s"found $nwords words!")
    val widest = results.map(x => x.length).max

    // print out the results sorted vertically in columns

    val sortedArr = results.sorted.toArray
    val nrows: Int = (nwords + (Board.displayColumns - 1)) / Board.displayColumns

    for (r <- 0 until nrows) {

      val row = for (i <- r until nwords by nrows) yield sortedArr(i)
      row.foreach (w => {
        print(w)
        print(" " * (widest - w.length + 5))
      })
      println
    }

  }
}

object Boggle {
  def main(args: Array[String]): Unit = {
    val board = new Board()
    board.play()
  }
}