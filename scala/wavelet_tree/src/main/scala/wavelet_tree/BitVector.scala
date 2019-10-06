package wavelet_tree

class BitVector(nums: Array[Int], mask: Int) {
  val bits = nums.map(e => if ((e & mask) == 0) 0 else 1)
  val vals = nums
  val zeroesBefore = Array.fill[Int](bits.length)(0)
  val onesBefore = Array.fill[Int](bits.length)(0)

  var zeroesSeen = 0
  var onesSeen = 0
  for (i <- bits.indices) {
    zeroesBefore(i) = zeroesSeen
    onesBefore(i) = onesSeen
    if (bits(i) == 0) {
      zeroesSeen += 1
    }
    else {
      onesSeen += 1
    }
  }

  def length(): Int = nums.length

  def partition(): (Array[Int], Array[Int]) = {
    nums.partition(x => (x & mask) == 0)
  }

  def zeroesPreceding(x: Int): Int = {
    // return the number of zeroes in the bv *before* position x (zero-based).
    // doesn't include x.
    zeroesBefore(x)
  }

  def onesPreceding(x: Int): Int = {
    // return the number of ones in the bv *before* position x (zero-based).
    // doesn't include x.
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

class Node(bitVector: BitVector) {
  var left: Option[Node] = None
  var right: Option[Node] = None

  def addChildren(leftArr: Array[Int], rightArr: Array[Int], mask: Int): Unit = {
    // proceed with recursion only if the left/right parts have > 1 unique elements

    if (mask == 0) return

    if (leftArr.length > 0) {
      val numUniques = leftArr.groupBy(identity).size
      val bv = new BitVector(leftArr, mask)
      val leftNode = new Node(bv)
      left = Some(leftNode)
      if (numUniques > 1) {
        val (leftPart, rightPart) = bv.partition()
        leftNode.addChildren(leftPart, rightPart, mask >> 1)
      }
    }

    if (rightArr.length > 0) {
      val numUniques = rightArr.groupBy(identity).size
      val bv = new BitVector(rightArr, mask)
      val rightNode = new Node(bv)
      right = Some(rightNode)
      if (numUniques > 1) {
        val (leftPart, rightPart) = bv.partition()
        rightNode.addChildren(leftPart, rightPart, mask >> 1)
      }
    }
  }

  def dump(depth: Int): Unit = {
    print(" " * depth)
    println(bitVector.bits.mkString(" "))

    left match {
      case Some(x) => x.dump(depth + 1)
      case _ =>
    }

    right match {
      case Some(x) => x.dump(depth + 1)
      case _ =>
    }
  }

  def subrangeMedian(from: Int, to: Int, rank: Int): Int = {

    val nzeroes = bitVector.zeroesInRange(from, to)

    if (nzeroes >= rank) {
      // it's on the 0 side
      val newFrom = bitVector.zeroesPreceding(from)
      val newTo = newFrom + nzeroes - 1

      left match {
        case Some(x) => x.subrangeMedian(newFrom, newTo, rank)
        case None => bitVector.vals(from)
      }
    }
    else {
      // it's on the 1 side
      val newFrom = bitVector.onesPreceding(from)
      val newTo = newFrom + bitVector.onesInRange(from, to) - 1

      right match {
        case Some(x) => x.subrangeMedian(newFrom, newTo, rank - nzeroes)
        case None => bitVector.vals(from + nzeroes)
      }
    }
  }
}

object WaveletTree {
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

class WaveletTree(nums: Array[Int]) {

  // how many bits in the largest member of nums?
  val bitwidth = WaveletTree.width(nums.max)
  val mask = 1 << (bitwidth - 1)
  val depth = 0
  val bv = new BitVector(nums, mask)
  val root = new Node(bv)

  val (leftArr, rightArr) = bv.partition()

  root.addChildren(leftArr, rightArr, mask >> 1)

  def dump(): Unit = {
    root.dump(depth)
  }

  def subrangeMedian(from: Int, to: Int): Int = {
    val rank = (to - from) / 2 + 1
    root.subrangeMedian(from, to, rank)
  }
}