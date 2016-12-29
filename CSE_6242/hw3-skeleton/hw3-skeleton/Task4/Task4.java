package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Task4 {

  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    private final static IntWritable count= new IntWritable();
    private Text word = new Text();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      int x=0
      while (itr.hasMoreTokens()) {
	String wrd=itr.nextToken()
	if (x==1){
        word.set(wrd);}
	if (x==2){
	count.set(Integer.parseInt(wrd));}
        x=x+1;
        context.write(word, count);
      }
    }

  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int max = 0;
      for (IntWritable count : values) {
        int value= count.get();
	if (value>max){
		max=value
	}
      }
      result.set(max);
      context.write(key, result);
    }
  }

  public static class DataMapper
		 extends Mapper<Object, Text, Text, IntWritable>{

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException{
		String vals[]=value.toString().split("\t");
		context.write(new IntWritable(Integer.parseInt(vals[1])),new IntWritable(1));
}
}

  public static class DegreeReducer
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {

  public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
		       ) throws IOException, InterruptedException {
      int i = 0;
      for (IntWritable count : values) {
        i+=count.get();
	}
      }
      result.set(i);
      context.write(key, result);
    }


  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job1 = Job.getInstance(conf, "Task4");

    /* TODO: Needs to be implemented */
    job1.setJarByClass(Task4.class);
    job1.setMapperClass(TokenizerMapper.class);
    job1.setCombinerClass(IntSumReducer.class);
    job1.setReducerClass(IntSumReducer.class);
    job1.setOutputKeyClass(Text.class);
    job1.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, new Path(args[1]));
    System.exit(job1.waitForCompletion(true) ? 0 : 1);

    Configuration conf = new Configuration();
    Job job2 = Job.getInstance(conf, "Task4");

    /* TODO: Needs to be implemented */
    job2.setJarByClass(Task4.class);
    job2.setMapperClass(DataMapper.class);
    job2.setCombinerClass(DegreeReducer.class);
    job2.setReducerClass(DegreeReducer.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job2, new Path(args[0]));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}
