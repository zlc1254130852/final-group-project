var log=[]
var chatFrame;
var id=""
var counter=0;
var system=""
			window.onload = function () {
			    id=document.getElementById('id')
				log=JSON.parse(localStorage.getItem(id.innerHTML));
				if (log==null)
					log=[]

				document.getElementById('stopButton').disabled=true

				document.getElementById('myquestion').style.marginBottom="-22px"
				document.getElementById('sendButton').style.marginBottom="20px"
				document.getElementById('stopButton').style.marginBottom="20px"
				document.getElementById('clearButton').style.marginBottom="20px"

				chatFrame=document.getElementById("parent")

				setTimeout(function(){
					chatFrame.scrollTop = chatFrame.scrollHeight;
				},0);

				for (var i=0;i<log.length;i++)
				{
					addElementDiv(log[i].content,counter,log[i].role);
					counter+=1
				}
			}
			
			function addElementDiv(message,counter,speaker){
				var parent = document.getElementById("parent")
				if (parent==null)
					console.log("empty")
				let div_0 = document.createElement("div")
				div_0.setAttribute("class","clearfix")
				let div0 = document.createElement("div")
				let div00 = document.createElement("br")
				let div01 = document.createElement("br")
				let div1 = document.createElement("div")
				div0.setAttribute("id","div0"+counter.toString())
				div1.setAttribute("id","div"+counter.toString())

				div1.style.maxWidth = "250px"
				div1.style.backgroundColor = "#90EE90";
				div1.style.border = "1px solid black";
				div1.style.textAlign = "left";
				div1.style.padding = "2px"
				div1.style.whiteSpace = "pre-line"

				if (speaker==="user"){
					div0.style.float = "right";
					div00.style.float = "right";
					div1.style.float = "right";
				}
				else{
					div0.style.float = "left";
					div00.style.float = "left";
					div1.style.float = "left";
				}
				div1.style.borderRadius = "5px";
				div0.innerHTML=speaker;
				div1.innerHTML=message;

				parent.appendChild(div_0)
				parent.appendChild(div0)
				parent.appendChild(div00)
				parent.appendChild(div1)
				parent.appendChild(div01)
			}
			var stop=1
			function chat(opt){
				tmp_question=$("#myquestion").val()
				system=$("#system").val()
				if (tmp_question.trim()=="")
					return

				document.getElementById('sendButtonArea').hidden=true
				document.getElementById('stopButtonArea').hidden=false

				document.getElementById('stopButton').disabled=false
				stop=0
				document.getElementById('myquestion').disabled="disabled"
				document.getElementById('sendButton').disabled="disabled"
				document.getElementById('clearButton').disabled=true

				log.push({"role": "user", "content": tmp_question});
				document.getElementById('myquestion').value="";
				addElementDiv(tmp_question,counter,"user");
				setTimeout(function(){
					chatFrame.scrollTop = chatFrame.scrollHeight;
				},0);
				counter+=1
				localStorage.setItem(id.innerHTML,JSON.stringify(log))
				var n = 5
				//$("#chatResponse").text(log);
				content=""

				fetch('/chat', {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({option:opt,system:system,question:tmp_question,history:JSON.stringify(log.slice(-n))}),
				}).then(response => {
					const reader = response.body.getReader();
					const decoder = new TextDecoder('utf-8');
					let buffer = '';
					addElementDiv("",counter,"assistant");
					var show=document.getElementById('div'+counter.toString())
					counter+=1

					function processStreamResult(result2) {
						const chunk = decoder.decode(result2.value, { stream: !result2.done });
						buffer += chunk;

						const lines = buffer.split('\n');
						buffer = lines.pop();

						lines.forEach(line => {
							if (line.trim().length > 0) {

								if(stop==1){
//									log.push({"role": "assistant", "content": content});
//									localStorage.setItem(id.innerHTML,JSON.stringify(log))
//									document.getElementById('myquestion').disabled=false
//									document.getElementById('sendButton').disabled=false
//									document.getElementById('clearButton').disabled=false
//									document.getElementById('stopButton').disabled=true
//									document.getElementById('sendButton').hidden=false
//									document.getElementById('stopButton').hidden=true
								}else{
									var obj=JSON.parse(line)
									var obj1=obj.choices[0].delta.content
									var obj2=obj.choices[0].finish_reason
									if (obj2!=null){
										log.push({"role": "assistant", "content": content});
										localStorage.setItem(id.innerHTML,JSON.stringify(log))
										document.getElementById('myquestion').disabled=false
										document.getElementById('sendButton').disabled=false
										document.getElementById('clearButton').disabled=false
										document.getElementById('stopButton').disabled=true
										document.getElementById('sendButtonArea').hidden=false
										document.getElementById('stopButtonArea').hidden=true
									} else if(obj1!=null){
										content += obj1
										show.innerHTML = content;
										//console.log(obj1);

										chatFrame.scrollTop = chatFrame.scrollHeight;
									}
									//console.log(line);
								}

							}
						});

						if (!result2.done && stop==0) {
							return reader.read().then(processStreamResult);
						}
					}

					return reader.read().then(processStreamResult);
				})
						.catch(error => {
							console.error('Error:', error);
						});
			}
			function abortStream(opt){
				stop=1
				$.ajax({
					url: "/abort",
					method: "GET",
					data: {
						option: opt
					},
					success: function(response) {
					}
				});
				log.push({"role": "assistant", "content": content});
				localStorage.setItem(id.innerHTML,JSON.stringify(log))
				document.getElementById('myquestion').disabled=false
				document.getElementById('sendButton').disabled=false
				document.getElementById('clearButton').disabled=false
				document.getElementById('stopButton').disabled=true
				document.getElementById('sendButtonArea').hidden=false
				document.getElementById('stopButtonArea').hidden=true
			}
			function clearChat(){
				localStorage.removeItem(id.innerHTML)
				log=[]
				var pObjs = chatFrame.childNodes;
				for (var i = pObjs.length - 1; i >= 0; i--) {
					chatFrame.removeChild(pObjs[i]);
				}
			}
