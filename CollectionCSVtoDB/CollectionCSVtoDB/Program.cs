    using System;
using System.Collections.Generic;
using System.IO;

namespace CollectionCSVtoDB
{
    class Program
    {
        static void Main(string[] args)
        {
            string input = "placeholder";
            string output = "placeholder";

            if (args.Length != 0)
            {
                input = args[0];
                output = args[1];
            }
            else
            {
                Console.WriteLine("Enter Input Path:");
                input = Console.ReadLine();
                Console.WriteLine("Enter Output Path:");
                output = Console.ReadLine();
            }
            string fileName = Path.GetFileNameWithoutExtension(input);
            string[] lines = System.IO.File.ReadAllLines(input);
            List<string> md5 = new List<string>();
            foreach (string line in lines)
            {
                var values = line.Split(",");
                md5.Add(values[2]);
            }
            int length = md5.Count;
            BinaryWriter BinWriter = new BinaryWriter(File.Create(output));
            BinWriter.Write((int)DateTime.Now.Ticks);
            BinWriter.Write(1);
            BinWriter.Write((byte)0x0b);
            BinWriter.Write(fileName);
            BinWriter.Write(length);
            for (int i=0; i<length; i++) {
                BinWriter.Write((byte)0x0b);
                BinWriter.Write(md5[i]);
            }
            BinWriter.Close();
        }
    }
}
