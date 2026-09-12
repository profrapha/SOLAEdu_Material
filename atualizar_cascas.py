import os

raiz_projeto = os.path.dirname(os.path.abspath(__file__))

def gerar_conteudo_aluno(nome_base):
    return (
        "% !TEX output_directory = ../publica\n"
        "\\documentclass[twoside, 10pt, a4paper]{article}\n\n"
        "% --- DECLARAÇÃO SEGURA DA VARIÁVEL DE GABARITO ---\n"
        "\\newif\\ifgabarito\n"
        "\\gabaritofalse\n\n"
        f"\\input{{{nome_base}}}\n"
    )

def gerar_conteudo_prof(nome_base):
    return (
        "% !TEX output_directory = ../restrita\n"
        "\\documentclass[twoside, 10pt, a4paper]{article}\n\n"
        "% --- DECLARAÇÃO SEGURA DA VARIÁVEL DE GABARITO ---\n"
        "\\newif\\ifgabarito\n"
        "\\gabaritotrue\n\n"
        f"\\input{{{nome_base}}}\n"
    )

total_criados = 0
total_corrigidos = 0

for pasta_atual, _, arquivos in os.walk(raiz_projeto):
    if os.path.basename(pasta_atual) == "fonte_tex":
        tex_files = [f for f in arquivos if f.endswith(".tex")]

        # Identifica todas as bases existentes na pasta
        bases = [f for f in tex_files if f.endswith("_BASE.tex")]

        # Se houver apenas 1 arquivo .tex e for _ALUNO, ele é a base original
        if len(tex_files) == 1 and tex_files[0].endswith("_ALUNO.tex"):
            arq_antigo = tex_files[0]
            prefixo = arq_antigo.replace("_ALUNO.tex", "")
            nome_base = f"{prefixo}_BASE.tex"
            
            caminho_antigo = os.path.join(pasta_atual, arq_antigo)
            caminho_base = os.path.join(pasta_atual, nome_base)
            
            os.rename(caminho_antigo, caminho_base)
            print(f"[RENOMEADO PARA BASE] {arq_antigo} -> {nome_base}")
            bases.append(nome_base)
            tex_files = [nome_base]

        # Para cada base encontrada, assegura a existência das cascas ALUNO e PROF
        for base in bases:
            prefixo = base.replace("_BASE.tex", "")
            nome_aluno = f"{prefixo}_ALUNO.tex"
            nome_prof = f"{prefixo}_PROF.tex"

            caminho_aluno = os.path.join(pasta_atual, nome_aluno)
            caminho_prof = os.path.join(pasta_atual, nome_prof)

            if not os.path.exists(caminho_aluno):
                with open(caminho_aluno, "w", encoding="utf-8") as f:
                    f.write(gerar_conteudo_aluno(base))
                print(f"[CRIADO CASCA ALUNO] {nome_aluno}")
                total_criados += 1

            if not os.path.exists(caminho_prof):
                with open(caminho_prof, "w", encoding="utf-8") as f:
                    f.write(gerar_conteudo_prof(base))
                print(f"[CRIADO CASCA PROF]  {nome_prof}")
                total_criados += 1

        # Garante as diretivas nos arquivos que já existiam
        for arq in [f for f in tex_files if not f.endswith("_BASE.tex")]:
            caminho = os.path.join(pasta_atual, arq)
            if arq.endswith("_ALUNO.tex"):
                with open(caminho, "r", encoding="utf-8") as f:
                    c = f.read()
                if not c.strip().startswith("% !TEX output_directory"):
                    with open(caminho, "w", encoding="utf-8") as f:
                        f.write("% !TEX output_directory = ../publica\n" + c)
                    total_corrigidos += 1
            elif arq.endswith("_PROF.tex"):
                with open(caminho, "r", encoding="utf-8") as f:
                    c = f.read()
                if not c.strip().startswith("% !TEX output_directory"):
                    with open(caminho, "w", encoding="utf-8") as f:
                        f.write("% !TEX output_directory = ../restrita\n" + c)
                    total_corrigidos += 1

print(f"\nFinalizado com sucesso!")
print(f"- Cascas novas geradas: {total_criados}")
print(f"- Diretivas verificadas/corrigidas: {total_corrigidos}")