package sudoku

import org.scalatest.FunSuite

class SudokuTest extends FunSuite {

  test("row to cell - (0, 1, 2)") {
    val sz = 4
    val sdk = new Sudoku(sz)

    val row = sdk.cellToRow(0, 1, 2)
    val (r, c, v) = sdk.rowToCell(row)

    assert(r === 0)
    assert(c === 1)
    assert(v === 2)

    assert((r, c, v) === (0, 1, 2))
    // 2 0 4, 3 1 1
  }

  test("row to cell - (2, 0, 4)") {
    val sz = 4
    val sdk = new Sudoku(sz)

    val row = sdk.cellToRow(2, 0, 4)
    val (r, c, v) = sdk.rowToCell(row)

    // cell                  row                   column                region
    // 0000-0000-1000-0000   0000-0000-0001-0000   0001-0000-0000-0000   0000-0000-0001-0000
    println(row)
    assert(r === 2)
    assert(c === 0)
    assert(v === 4)

    assert((r, c, v) === (2, 0, 4))
    // 2 0 4, 3 1 1
  }

  test("row to cell - (3, 1, 1)") {
    val sz = 4
    val sdk = new Sudoku(sz)

    val row = sdk.cellToRow(3, 1, 1)
    val (r, c, v) = sdk.rowToCell(row)

    assert((r, c, v) === (3, 1, 1))
  }
}
