import dados
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

biblioteca = dados.carregar_do_arquivo()


@app.route('/')
def index():
    return render_template('index.html', livros=biblioteca)


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


@app.route('/biblioteca/delete/<isbn>', methods=['POST'])
def deletar_livro(isbn):
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            biblioteca.remove(livro)
            dados.salvar_no_arquivo(biblioteca)
            return jsonify('Livro deletado com sucesso')
    return jsonify('Livro não encontrado'), 404



@app.route('/biblioteca/update/<isbn>', methods=['GET'])
def exibir_livro(isbn=None, opcao=None):
        livro_encontrado = None
        for l in biblioteca:
            if l['isbn'] == isbn:
                livro_encontrado = l
                break
    
        if not livro_encontrado:
            return jsonify("Livro não encontrado com este ISBN.")
        
        return render_template('editar.html', livro=l)



@app.route('/biblioteca/update/<isbn>', methods=['POST'])
def atualizar_livro(isbn=None, opcao=None):
    livro_encontrado = None
    for l in biblioteca:
        if l['isbn'] == isbn:
            livro_encontrado = l
            break
    
    if not livro_encontrado:
        erro = 'Não existe um livro com este ISBN!'
        return render_template('cadastrar.html', erro=erro)
    
    edicoes = {
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'genero': request.form['genero'],
        'ano_publicacao': int(request.form['ano_publicacao']),
        'editora': request.form['editora'],
        'paginas': int(request.form['paginas']),
        'status': 'disponivel',
        'localizacao': request.form['localizacao']
    }

    for chave in edicoes:
        if chave in edicoes:
            novo_valor = edicoes[chave]

            if chave in ["ano_publicacao", "paginas"]:
                try:
                    novo_valor = int(novo_valor)
                except ValueError:
                    erro = "Erro: Este campo deve ser um número inteiro. Operação cancelada."
                    return render_template('cadastrar.html', erro=erro)

            livro_encontrado[chave] = novo_valor
        else:
            erro = "Opção inválida."
            return render_template('cadastrar.html', erro=erro)

    dados.salvar_no_arquivo(biblioteca)
    return render_template('editar.html', livro=l)


if __name__ == "__main__":
    app.run(debug=True)