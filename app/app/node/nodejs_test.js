// https://javafa.gitbooks.io/nodejs_server_basic/content/chapter9.html 참고 


var http = require('http');
// 1. 요청한 url을 객체로 만들기 위해 url 모듈사용
var url = require('url');
// 2. 요청한 url 중에 Query String 을 객체로 만들기 위해 querystring 모듈 사용
var querystring = require('querystring'); 
var fs = require('fs');

var server = http.createServer(function(request,response){
        // 4. 브라우저에서 요청한 주소를 parsing 하여 객체화 후 출력
        var parsedUrl = url.parse(request.url);
        console.log(parsedUrl);
        var resource = parsedUrl.pathname;
        console.log(resource);

        // POST 요청 처리
        // 1. post로 전달된 데이터를 담을 변수를 선언
        console.log("====<POST START>====");
        var postdata = '';
        // 2. request객체에 on( ) 함수로 'data' 이벤트를 연결
        request.on('data', function (data) {
                // 3. data 이벤트가 발생할 때마다 callback을 통해 postdata 변수에 값을 저장
                postdata = postdata + data;
                console.log("post data = "+ postdata);

                var parsedQuery = querystring.parse(postdata);
                console.log("parsedQuery");
                console.log(parsedQuery);
                response.writeHead(200, {'Content-Type':'text/html'});
                response.end('var1의 값 = ' + parsedQuery.var1);

        });
        // request객체에 on( ) 함수로 'end' 이벤트를 연결
        request.on('end', function (postdata) {
                // 5. end 이벤트가 발생하면(end는 한버만 발생한다) 3번에서 저장해둔 postdata 를 querystring 으로 객체화
                var parsedQuery = querystring.parse(postdata);
                // 6. 객체화된 데이터를 로그로 출력
                console.log(parsedQuery);
                // 7. 성공 HEADER 와 데이터를 담아서 클라이언트에 응답처리
                response.writeHead(200, {'Content-Type':'text/html'});
                response.end(parsedQuery.var1);
        });
        console.log("====<POST END>====");


        // 1. 요청된 자원이 /hello 이면
        if(resource == '/hello'){
                // 2. hello.html 파일을 읽은 후
                fs.readFile('hello.html', 'utf-8', function(error, data) {
                        // 2.1 읽으면서 오류가 발생하면 오류의 내용을
                        if(error){
                                response.writeHead(500, {'Content-Type':'text/html'});
                                response.end('500 Internal Server Error : '+error);
                        // 2.2 아무런 오류가 없이 정상적으로 읽기가 완료되면 파일의 내용을 클라이언트에 전달
                        }else{
                                response.writeHead(200, {'Content-Type':'text/html'});
                                response.end(data);
                        }
                });
        }else{
                console.log("====<GET START>====");
                // 5. 객체화된 url 중에 Query String 부분만 따로 객체화 후 출력
                var parsedQuery = querystring.parse(parsedUrl.query,'&','=');
                console.log(parsedQuery);
                var result1 = parsedQuery.var1;
                console.log('전달된 var1의 값은 ' +result1+'입니다');

                response.writeHead(200, {'Content-Type':'text/html'});
                response.end('var1 value is '+parsedQuery.var1);
                console.log("====<GET END>====");
        }
});

server.listen(8000, function(){
        console.log('Server is running...');
});