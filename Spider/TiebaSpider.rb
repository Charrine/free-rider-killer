require 'net/http'

uri = URI('https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false')
response = Net::HTTP.get_response(uri)
cookie = response['set-cookie']
puts cookie



#puts login_result.code
#puts login_result.message
#puts login_result.class.name
#puts login_result.body




#Get method
#uri = URI('http://tieba.baidu.com/f?kw=c%D3%EF%D1%D4&fr=index')
#puts Net::HTTP.get(uri)

#Post method
#uri = URI('http://localhost/test.php')
#res = Net::HTTP.post_form(uri, 'p' => 1)
#puts res.body
