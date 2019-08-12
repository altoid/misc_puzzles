package boggle

import org.scalatest.FunSuite

class BoardTest extends FunSuite {
  test("basic") {
    assert(true)
  }

  test("generate board") {
    val board = new Board()
    board.display()
  }

  test("cell test") {
    val cell = Cell('A')
    println(cell)

    val cell2: Cell = 'B'
    println(cell2)
  }

  test("dict test") {
    val board = new Board()
    if (board.all_words.hasNext) {
      println(board.all_words.next())
    }
  }
}
