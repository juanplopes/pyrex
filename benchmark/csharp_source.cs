using System;
using System.Text.RegularExpressions;

class MainClass
{
	public static void Main (string[] args)
	{
		var r = new Regex (Console.ReadLine ());

		string input;
		while ((input = Console.ReadLine()) != null) {
			long start = DateTime.Now.Ticks;
			r.Match(input);
			Console.WriteLine((DateTime.Now.Ticks-start)*100);
		}
	}
}


