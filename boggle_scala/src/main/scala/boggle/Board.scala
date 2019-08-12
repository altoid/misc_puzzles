package boggle

import scala.io.Source
import scala.util.Random

class Cell(l: Char) {
    val letter = l
    var visited: Boolean = false

  override def toString: String = letter.toString
}

object Cell {
  def apply(letter: Char): Cell = new Cell(letter)

  implicit def toCell(letter: Char) = Cell(letter)
}

class Board {
  private val alphabet = "abcdefghijklmnoprstuvwxyz".toCharArray // q is omitted
  private val size = 4

  private val tableau: Array[Cell] = Array.fill[Cell](size * size)(alphabet(Random.nextInt(alphabet.length)))

  val all_words: Iterator[String] = Source.fromResource("all.txt").getLines()

  def display(): Unit = {
    for (i <- 0 until size) {
      for (j <- 0 until size) {
        print(tableau(i * size + j) + " ")
      }
      println
    }
  }
}
