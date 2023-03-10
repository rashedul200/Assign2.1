import openai
import base64
import requests



wp_user = 'rasheduli'
website_url = 'https://mypracticesitecom.local'
wp_pass = 'f48V sVzL sIfY v99Y nJrf eXLr'
url = website_url +'/wp-json/wp/v2'


token = base64.standard_b64encode((wp_user + ':' + wp_pass).encode('utf-8')) # we have to encode the usr and pw
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}


def text_render(command):
  openai.api_key = 'sk-rpW54XchxIglIYKGht0I5T3BlbkFJwfldoi3CAWXBlWK8qEMsrn'
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt=command,
  temperature=0.7,
  max_tokens=1010,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
  return response["choices"][0]["text"].strip()
def text_formating(text):
    text = text.replace('.','.---').split('---')
    retun_text1 = '<!-- wp:paragraph --><p>' + ''.join(text[0:2]) + '</p><!-- /wp:paragraph -->'
    retun_text2 = '<!-- wp:paragraph --><p>' + ''.join(text[2:4]) + '</p><!-- /wp:paragraph -->'
    retun_text3 = '<!-- wp:paragraph --><p>' + ''.join(text[4:]) + '</p><!-- /wp:paragraph -->'
    return retun_text1+retun_text2+retun_text3
with open('mykeywords.txt', 'r+') as file:
  read_line = file.readlines()
  for keyword in read_line:
    final_outline = []
    outline = text_render(f'Write a blog outline for the following request from a customer.\n\nREQUEST:{keyword}\n\nBrainstorm a list of sections for this blog post. The outline should meet the customer\'s request and each section should be highly descriptive.\n\nSECTIONS:\n\n1.')
    improve_outline = text_render(f'I brainstormed the following list of sections of a blog based on the customer\'s request. I need to brainstorm to see if there are any improvements I can make to this outline.\n\nREQUEST:{keyword}\n\nOUTLINE:\n{outline}\n\nBrainstorm some possible improvements:\n\n1.')
    update_outline = improve_outline.splitlines()
    for x in update_outline:
      if len(x) > 0 and "Introduction" not in x and "Conclusion" not in x:
        final_outline.append(x.replace('1.','').replace('2.','').replace('3.','').replace('4.','').replace('5.','').replace('6.','').replace('7.','').replace('8.','').replace('9.','').replace('10.','').strip())
    post_intro = '<!-- wp:paragraph --><p>'+text_render(f'Write high blog introduction, Topic:{keyword}:')+'</p><!-- /wp:paragraph -->'
    body = post_intro
    for x in final_outline:
      heading = f'<!-- wp:heading --><h2>{x}</h2><!-- /wp:heading -->' + text_formating(text_render(f'"""\nBlog Section Title: {x}, Main Keyword: {keyword}\n"""\nWrite this blog section into a details professional para, witty and clever explanation:'))
      body += heading


    wp_title = keyword
    content = body
    slug = keyword.replace(' ','-')

    post = {'title': wp_title,
            'slug': slug,
            'status': 'draft',
            'content': content,
            'categories':'1',
            'author': '1',
            'format': 'standard',
            }
    r = requests.post(url + '/posts', headers=headers, json=post,verify=False)
    print(r.status_code)