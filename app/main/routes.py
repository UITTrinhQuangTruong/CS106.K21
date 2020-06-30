from flask import render_template, current_app, redirect, url_for, flash, request,jsonify
from app.main.forms import SearchForm
from app.main import bp
from flask import g
from pysesame import connection

key = ['Khái niệm', 'Thuộc chương', 'Cách cài đặt', 'Ý tưởng', 'Độ phức tạp của thuật toán', 'Tên chương', 'Cài đặt']
def clear_string(text):
	text = text.replace("_", " ")
	text = text.replace("\\t", "----")
	return text

def get_me(text):

#Thiết lập kết nối, tạo đối tượng (phải có)
	con = connection('http://localhost:8080/openrdf-sesame/')
	con.use_repository('Final_course')
	res2=con.query_one_para(text)
	#Query 1 biến in ra tất cả mọi thứ thuộc về chủ đề
	res=con.query_remove_para(text, 'namedindividual')
	i = 0
	n = len(res)
	me1 =set()
	separator = "\n"
	while  i < n:
		temp = clear_string(separator.join(res[i]))
		res[i] = [j for j in temp.split("\n")]
		
		if res[i][0].lower() != text.lower():
			me1.add(res[i][0])
			res.pop(i)
			n -= 1
		else:
			if res[i][1] not in key:
				me1.add(res[i][2])
				res.pop(i)
				n -= 1
			else:
				i += 1


	#Query 2 biến in ra chủ đề và liên kết của chủ đề 

	res1=con.query_two_para('Cây', text)

	#Query 2 biến lọc liên kết trong tham số 2
	
	return res, me1
	#Các liên kết tiếng việt có thể nhập vào 
	#{con của lớp': 'subClassOf', 'khái niệm': 'isDefinedBy','loại':'@type','miền giá trị': 'domain'}

	#các liên kết khác vẫn có thể nhập, miễn là nhập đúng
	#lưu ý trong ontology tất cả các liên kết đều phải viết thường

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html', title='Home Page')

@bp.route('/about')
def about():
    return  render_template('about.html', title='About Us')

@bp.route('/search')
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	posts = g.search_form.q.data
	me, me1 = get_me(posts)
	return render_template('search.html', title=('Search'), me=me, me1=me1)

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()
