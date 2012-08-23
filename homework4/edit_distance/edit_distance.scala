object EditDistance {
  def levenshteinDistance(s: String, t: String): Int = {
    val m = s length
    val n = t length
    var d = Array.ofDim[Int](m+1,n+1)

    for (i <- 0 until m+1) {
      d(i)(0) = i
    }

    for (j <- 0 until n+1) {
      d(0)(j) = j
    }

    for (i <- 0 until m) {
      for (j <- 0 until n) {
        if (s(i) == t(j)) {
          d(i+1)(j+1) = d(i)(j)
        } else {
          d(i+1)(j+1) = List(
            d(i)(j+1) + 1, // deletion
            d(i+1)(j) + 1, // insertion
            d(i)(j) + 1    // substitution
          ).min
        }
      }
    }

    d(m)(n)
  }

  def main(args: Array[String]) = {
    if (args.length == 0) {
      println("USAGE: scala edit_distance.scala STRING1 STRING2")
    }
    println(levenshteinDistance(args(0), args(1)))
  }
}
