import dados
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

biblioteca = dados.carregar_do_arquivo()


@app.route('/')
def index():
    biblioteca_atual = dados.carregar_do_arquivo()
    return render_template('index.html', livros=biblioteca_atual)


@app.route('/cadastrar', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastrar.html')


@app.route('/cadastrar', methods=['POST'])
def salvar_cadastro():
    isbn = request.form['isbn']

    for livro in biblioteca:
        if livro['isbn'] == isbn:
            erro = 'Já existe um livro com este ISBN!'
            return render_template('cadastrar.html', erro=erro)

    novo_livro = {
        'isbn': isbn,
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'genero': request.form['genero'],
        'ano_publicacao': int(request.form['ano_publicacao']),
        'editora': request.form['editora'],
        'paginas': int(request.form['paginas']),
        'status': 'disponivel',
        'localizacao': request.form['localizacao']
    }

    biblioteca.append(novo_livro)
    dados.salvar_no_arquivo(biblioteca)

    mensagem = 'Livro cadastrado com sucesso!'
    return render_template('cadastrar.html', mensagem=mensagem)


@app.route('/biblioteca', methods=['GET'])
def exibir_json():
    return jsonify(biblioteca), 200


@app.route('/biblioteca/insert', methods=['POST'])
def inserir_livro():
    novo_livro = request.get_json()
    biblioteca.append(novo_livro)
    dados.salvar_no_arquivo(biblioteca)
    return jsonify('Novo livro inserido'), 201


@app.route('/biblioteca/<isbn>')
def achar_isbn(isbn):
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            return jsonify(livro)
    return jsonify('Livro não encontrado'), 404


@app.route('/biblioteca/delete/<isbn>', methods=['DELETE'])
def deletar_livro(isbn):
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            biblioteca.remove(livro)
            dados.salvar_no_arquivo(biblioteca)
            return jsonify('Livro deletado com sucesso')
    return jsonify('Livro não encontrado'), 404


if __name__ == "__main__":
    app.run(debug=True)