import roman.RomanNumeral

import scala.annotation.tailrec

object Misc {
  def genX(): IndexedSeq[Int] = {
    for {
      p <- (4 to 9)
      if (p % 2 == 0)
    } yield p
  }

  def combinations[A](n: Int, l: List[A]): List[List[A]] = {
    if (n > l.length) List[List[A]]()
    else if (n == 0 || l.length == 0) List(List[A]())
    else {
      val part1 = combinations(n - 1, l.tail).map(x => l.head :: x)
      val part2 = combinations(n, l.tail)
      part1 ++ part2
    }
  }

  /* given a list of integers, return the permutation of those integers that immediately follows it.  examples:

  (1 2 3 4) => (1 2 4 3)
  (2 4 3 1) => (3 1 2 4)
  (4 3 2 1) => Nil

   algorithm:
   - scan right-to-left to first item x that is smaller than
     the one to its right
   - swap it with the smallest item to the right
     of x that is larger than x (y)
   - sort the list [x+1:]
   */
  def successor[A : Ordering](l: List[A]): List[A] = {
    val ordering = implicitly[Ordering[A]]

    @tailrec
    def index_of_swap_candidate(i: Int): Int = {
      // scan right-to-left to first item x that is smaller than
      // the one to its right.  return -1 if this condition cannot be met.
      //
      // ********* do not call this if l.length < 2 *********
      //

      if (i < 0) -1
      else {
        if (ordering.lt(l(i), l(i + 1))) i
        else index_of_swap_candidate(i - 1)
      }
    }

    def index_of_least_greater_element_right_of(i: Int): Int = {
      if (i < 0) -1
      else if (i == l.length - 1) -1
      else {
        var j = i + 1
        var answer = j
        var m = l(j) // we know this is bigger than l(i)
        while (j < l.length) {
          if (ordering.lt(l(i), l(j)) && ordering.lt(l(j), m)) {
            m = l(j)
            answer = j
          }
          j += 1
        }
        answer
      }
    }

    if (l.length < 2) return Nil

    val k = index_of_swap_candidate(l.length - 2)

    if (k < 0) Nil
    else {
      val x = index_of_least_greater_element_right_of(k)
      if (x < 0) Nil
      else {
        // create new list with elements at x and k swapped.  k < x
        val (a, b) = l.splitAt(k)
        val (c, d) = b.splitAt(x - k)

        val rest = (d.head :: c.tail) ::: (c.head :: d.tail)
        return a ::: (rest.head :: rest.tail.sorted)
      }
    }

    Nil
  }

  def testRoman = {
    println(new RomanNumeral("mdccclxxv").toInt()) // 1875
    //    println(romanToDecimal("mm"))
    //    println(romanToDecimal("mcm"))
    //    println(romanToDecimal("mc"))
    //    println(romanToDecimal("cm"))
    //    println(romanToDecimal("mmiii"))
    //    println(romanToDecimal("i"))
    //    println(romanToDecimal("v"))
    //    println(romanToDecimal("xii"))

    val cm = RomanNumeral("cm")
    val d = RomanNumeral("d")
    val x = RomanNumeral("x")
    val m = RomanNumeral("m")

    var rnums = List(cm, m, d, x).sorted

    while (rnums != Nil) {
      println(rnums)
      rnums = successor(rnums)
    }
  }

  def main(args: Array[String]): Unit = {
//    successor(List(1, 2, 3, 4)) foreach println
//    successor(List(1, 2, 4, 3)) foreach println
//
//    successor(List(4, 3, 2, 1)) foreach println
//
//    var l = List(1,2,3,4)
//    while (l != Nil) {
//      println(l)
//      l = successor(l)(Ordering[Int]) // Ordering[Int] has a companion object, which we pass here.
//    }


    testRoman
  }

}
