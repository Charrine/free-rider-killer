require 'rubygems'
require 'nokogiri'
require 'open-uri'

file = open("temp", "w")
pageNum = 100
pageNum.times do |i|
  page = Nokogiri::HTML(open("http://tieba.baidu.com/f?kw=c%E8%AF%AD%E8%A8%80&ie=utf-8&pn=#{i * 50}"))
  thread = page.css(".j_thread_list")

  thread.each do |thread|
    title = thread.css("a.j_th_tit").text
    abstract = thread.css("div.threadlist_abs").text
    if abstract == ''
      abstract = 'none'
    end
    puts title.encoding
    file.write("#{title}\n")
    file.write("#{abstract}\n")
  end

  puts "Page num: #{i + 1}"
end
