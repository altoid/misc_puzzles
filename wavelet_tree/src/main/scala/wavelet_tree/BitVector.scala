package wavelet_tree

object BitVector {
  def width(n: Int): Int = {
    // how many bits are needed to express this number?
    var counter = 0
    var n2 = n

    while (n2 > 0) {
      counter += 1
      n2 = n2 >> 1
    }
    counter
  }
}

class BitVector(nums: Array[Int], nth: Int) {
  // retrieve the nth order bit from each member of nums.  0 is the most significant bit.

  // how many bits in the largest member of nums?
  val width = BitVector.width(nums.max)
  val mask = 1 << (width - (nth + 1))

  val bits = nums.map(e => if ((e & mask) == 0) 0 else 1)

  val zeroesBefore = Array.fill[Int](bits.length)(0)
  val onesBefore = Array.fill[Int](bits.length)(0)

  var zeroesSeen = 0
  var onesSeen = 0
  for (i <- 0 until bits.length) {
    zeroesBefore(i) = zeroesSeen
    onesBefore(i) = onesSeen
    if (bits(i) == 0) {
      zeroesSeen += 1
    }
    else {
      onesSeen += 1
    }
  }

  def zeroesPreceding(x: Int): Int = {
    // return the number of zeroes in the bv *before* position x (zero-based).  doesn't include x.
    zeroesBefore(x)
  }

  def onesPreceding(x: Int): Int = {
    // return the number of ones in the bv *before* position x (zero-based).  doesn't include x.
    onesBefore(x)
  }

  // ranges are inclusive
  def zeroesInRange(from: Int, to: Int): Int = {
    val result = zeroesPreceding(to) - zeroesPreceding(from)

    if (bits(to) == 0) {
      result + 1
    }
    else {
      result
    }
  }

  def onesInRange(from: Int, to: Int): Int = {
    val result = onesPreceding(to) - onesPreceding(from)

    if (bits(to) == 1) {
      result + 1
    }
    else {
      result
    }
  }
}
