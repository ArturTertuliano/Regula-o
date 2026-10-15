from playwright.sync_api import sync_playwright, expect, TimeoutError
from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import re
import streamlit as st


def main():
    global value_inside
    global entry
    global var_checkbox
    global contador

    janela = tk.Tk()
    janela.title("Minha Primeira Janela")
    janela.geometry("400x300")

    contador = tk.Spinbox(
    janela,
    from_=1,       # Minimum value
    to=15,        # Maximum value
    increment=1,   # Step size
    width=5,
    font=("Arial", 12)
    )
    contador.pack()

    label = tk.Label(janela, text="Digite uma unidade:")
    label.pack(pady=5)
    # Campo de entrada
    entry = tk.Entry(janela, width=30)
    entry.pack(pady=5)

    options_list = ["ESPECIALIDADES", "PROCEDIMENTOS"]
    value_inside = tk.StringVar(janela)
    value_inside.set("Selecione uma opção")

    question_menu = tk.OptionMenu(janela, value_inside, *options_list)
    question_menu.pack()

    var_checkbox = tk.IntVar(value=0)  
    checkbox = tk.Checkbutton(
    janela,
    text="Lançar",
    variable=var_checkbox,
    onvalue=1,  # valor quando marcado
    offvalue=0, # valor quando desmarcado
    font=("Arial", 12)
    )
    checkbox.pack(pady=20)
    botao = tk.Button(janela, text="Clique Aqui", command=executar)
    botao.pack()
    janela.mainloop()


def executar():
    #selecionando se sera procedimentos ou especialidades
    espe_ou_proced = format(value_inside.get())
    buscar_unidade = entry.get()
    cont = int(contador.get()) + 1
    
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=False)  # Abre o Chrome em modo visual
        contexto = navegador.new_context()
        pagina = contexto.new_page()  # Cria uma nova página
        pagina1 = contexto.new_page()
        pagina2 = contexto.new_page()
        tentativa = True

        pagina.goto("https://pontapora.esaude.genesiscloud.tec.br/login")
        pagina1.goto("https://core.saude.ms.gov.br/r2/web/pt_BR/login")
        pagina2.goto("https://cid.api.br/")

        expect(pagina.get_by_role("link", name="Regulação").nth(1)).to_be_enabled(timeout=60000)
        expect(pagina.get_by_role("link", name="Regulação").nth(1)).to_be_visible(timeout=60000)
        pagina.get_by_role("link", name="Regulação").nth(1).click()

        


        time.sleep(2)
        while tentativa == True:
            try:
                
                if espe_ou_proced == 'PROCEDIMENTOS':
                    #selecionar a aba de procedimentos
                    elemento = pagina.get_by_role("link", name="Procedimentos").wait_for(timeout=5000)
                    pagina.get_by_role("link", name="Procedimentos").click()
                else:
                    elemento = pagina.get_by_role("link", name="Especialidade").wait_for(timeout=5000)
                    pagina.get_by_role("link", name="Especialidade").click()

                time.sleep(2)
                elemento = pagina.get_by_role("button", name=" Filtros 0 ").wait_for(timeout=5000)
                pagina.get_by_role("button", name=" Filtros 0 ").click()

                #elemento = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[4]/section[3]/div/div[1]/div/div').wait_for(timeout=5000)
                #pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[4]/section[3]/div/div[1]/div/div').click()
                
                elemento = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[4]/section[3]/div/div[1]/div/div').wait_for(timeout=5000)
                pagina.locator("xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[4]/section[3]/div/div[1]/div/div").click()

                elemento = pagina.locator('#filtro-mais-opcoes .autocomplete-estabelecimento-de-saude').wait_for(timeout=5000)
                pagina.locator('#filtro-mais-opcoes .autocomplete-estabelecimento-de-saude').fill(buscar_unidade)
                time.sleep(2)
                pagina.keyboard.press("Enter")
            
                break
            except TimeoutError:
                pagina.reload()

        time.sleep(2)
        repetir = 0
        retorno = False
        repetido = False
        tentativa_verficar_paciente = 0
        nome_repitido = 0
        while repetir == 0:
            telemedicina= False
            ceo_kayatt_nucleo = False
            nao_possui_procedimento = False
           
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[4]/div[1]/div['+str(cont)+']/div/div[4]/div/a[1]')).to_be_visible(timeout=60000)
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[4]/div[1]/div['+str(cont)+']/div/div[4]/div/a[1]')).to_be_enabled(timeout=60000)
            pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[4]/div/div['+str(cont)+']/div/div[4]/div/a[1]').click() 
        
            
            time.sleep(2)

            #selecionar nome
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[2]')).to_be_visible(timeout=60000)
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[2]')).to_be_enabled(timeout=60000)
            paciente = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[2]').text_content(timeout=60000)
            
            #selecionar sus
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[3]')).to_be_visible(timeout=60000)
            expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[3]')).to_be_enabled(timeout=60000)
            sus = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[3]').text_content(timeout=60000)
            print(sus)

            
            if sus != '-':
                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[4]')).to_be_visible(timeout=60000)
                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[4]')).to_be_enabled(timeout=60000)
                data = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[4]').text_content(timeout=60000)
                ano = data[6:]
                agora = datetime.now()

                idade = int(agora.year) - int(ano)
                print(idade)
                print(ano)

                #pegar telefone

                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[6]')).to_be_visible(timeout=60000)
                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[6]')).to_be_enabled(timeout=60000)
                telefone = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[6]').text_content(timeout=60000)
                print(telefone)


                #selecionando profissional e unidade solicitante
                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dt[3]')).to_be_visible(timeout=60000)
                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dt[3]')).to_be_enabled(timeout=60000)
                retorno = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dt[3]').text_content()

                if retorno == 'Solicitante':
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[3]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[3]')).to_be_enabled(timeout=60000)
                    profissional = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[3]').text_content()
                    
                    teste = profissional.split("\n ", 1)
                    parte1, parte2 = teste
                    profissional1 = parte1.rstrip()
                    unidade = parte2.lstrip()
                    
                    #pegar a especialidade
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]')).to_be_enabled(timeout=60000)
                    especialidade = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]').text_content()
                    print(especialidade)
                    if(especialidade.count("TOMOGRAFIA")):
                        print('possui tomografia')
                    #selecionando cid
                    if espe_ou_proced == 'PROCEDIMENTOS':
                        expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[10]')).to_be_visible(timeout=60000)
                        expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[10]')).to_be_enabled(timeout=60000)
                        cid = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[10]').text_content()
                    else:
                        #colocar um if para identificar se é do ceo, kayatt ou nucleo
                        #/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[12]
                        expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[11]')).to_be_visible(timeout=60000)
                        expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[11]')).to_be_enabled(timeout=60000)
                        cid = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[11]').text_content()
                    print(cid)
                                
                elif retorno == 'Retorno':
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[4]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[4]')).to_be_enabled(timeout=60000)
                    profissional = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[4]').text_content()
                    dias_retorno = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[3]').text_content()
                    teste = profissional.split("\n ", 1)
                    parte1, parte2 = teste
                    profissional1 = parte1.rstrip()
                    unidade = parte2.lstrip()

                    #pegar data que consultou
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]')).to_be_enabled(timeout=60000)
                    data_retorno = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[6]').text_content()
                    
                    #pegar a especialidade
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[7]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[7]')).to_be_enabled(timeout=60000)
                    especialidade = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[7]').text_content()
                    print(especialidade)
                    
                    #selecionando cid
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[12]')).to_be_visible(timeout=60000)
                    expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[12]')).to_be_enabled(timeout=60000)
                    cid = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/dl/dd[12]').text_content()
                    print(cid)
                  #pegar unidade que o paciente esta cadastrado
                
                try:
                    elemento = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[7]').wait_for(timeout=2000)
                    Unidade_cadastrada = pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/dl/dd[7]').text_content()
                    print(Unidade_cadastrada)
                except TimeoutError:
                
                    if unidade == '(NUCLEO AMPLIADO DE SAUDE SONIA CINTAS)':
                        Unidade_cadastrada = 'Nada'
                    if unidade == '(CENTRO REGIONAL DE ESPECIALIDADE DR JOAO KAYATT)':
                        Unidade_cadastrada = 'Nada'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA ANDERSON LUIZ M GODOY)':
                        Unidade_cadastrada = 'Nada'
                    if unidade == '(CENTRO DE ATENDIMENTO MEDICO AMBULATORIAL - CIS)':
                        Unidade_cadastrada = 'CIS'
                    if unidade == '(CENTRO DE ESPECIALIDADE ODONTOLOGICA)':
                        Unidade_cadastrada = 'CENTRAL DE REGULACAO DE PONTA PORA'

                #Verificar se paciente possui unidade registrada
                if Unidade_cadastrada != 'Nada':
                
                    #substituir o nome do profissional pelo crm
                    if profissional1 == 'CAROLINA BARBEIRO FALEIRO COLLA':
                        profissional1 = '8916'
                    #substituir nome das unidades do esaude para o core
                    if unidade == '(CENTRO REGIONAL DE ESPECIALIDADE DR JOAO KAYATT)':
                            unidade = '('+Unidade_cadastrada.upper()+')'
                            ceo_kayatt_nucleo = True
                    if unidade == '(NUCLEO AMPLIADO DE SAUDE SONIA CINTAS)':
                            unidade = '('+Unidade_cadastrada.upper()+')'
                            ceo_kayatt_nucleo = True
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA ANDERSON LUIZ M GODOY)':
                        if profissional1 == 'PAOLA VILLANUEVA LUPOLI':
                            unidade = '('+Unidade_cadastrada.upper()+')'
                            telemedicina = True
                            print('verificar se deu certo: '+unidade)
                        else:
                            unidade = 'VILA AUREA'
                    if unidade == '(UNIDADE BASICA DE SAUDE ANDERSON LUIZ MONTEIRO GODOY)':
                        unidade = 'VILA AUREA'
                    if unidade == '(UNIDADE BASICA DE SAUDE ZENEIDA TERRA DE SIQUEIRA)':
                        unidade = 'ZENEIDA'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA ZENEIDA TERRA DE SIQUEIRA)':
                        unidade = 'ZENEIDA'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA ROSANGELA PEREIRA SILVA)':
                        unidade = 'ITAMARATI'
                    if unidade == '(UNIDADE BASICA DE SAUDE ROSANGELA PEREIRA SILVA)':
                        unidade = 'ITAMARATI'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA DR NERY DE AZAMBUJA)':
                        unidade = 'NERY'
                    if unidade == '(UNIDADE BASICA DE SAUDE DR NERY ALVES DE AZAMBUJA)':
                        unidade = 'NERY'
                    if unidade == '(UNIDADE BASICA DESAUDE DA FAMILIA DR CARLOS AUGUSTO PISSINI)':
                        unidade = 'ISSINI'
                    if unidade == '(UNIDADE BASICA DE SAUDE DR CARLOS AUGUSTO PISSINI SOBREIRO)':
                        unidade = 'ISSINI'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA LEONOR COELHO BATISTA)':
                        unidade = 'LEONOR COELHO'
                    if unidade == '(UNIDADE BASICA DE SAUDE LEONOR COELHO BATISTA)':
                        unidade = 'LEONOR COELHO'
                    if unidade == '(CENTRO INTEGRADO DE SAUDE CIS TERTULIANA DE FREITAS)':
                        unidade = 'CIS'
                    if unidade == '(CENTRO DE ATENDIMENTO MEDICO AMBULATORIAL - CIS)':
                        unidade = 'CIS'
                    if unidade == '(UNIDADE BASICA DA FAMILIA DRA NISLAINE COLMAN BENITES)':
                        unidade = 'NISLAINE COLMAN'
                    if unidade == '(UNIDADE BASICA DE SAUDE DRA NISLAINE COLMAN BENITES)':
                        unidade = 'NISLAINE COLMAN'
                    if unidade == '(UNIDADE PRISIONAL FEMININA DE PONTA PORA)':
                        unidade = 'PRISIONAL FEMININA'
                    if unidade == '(UNIDADE BASICA DE SAUDE EMERSON JOSE HARTINGER)':
                        unidade = 'EMERSON JOSE HARTINGER'
                    if unidade == '(SECRETARIA MUNICIPAL DE SAUDE DE PONTA PORA)':
                        unidade = 'SECRETARIA DE SAUDE'
                    if unidade == '(SERVICO AMBULATORIAL ESPECIALIZADO SAE)':
                        unidade = 'SERVICO AMBULATORIAL'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA NELSON MACHADO DIAS)':
                        unidade = 'POSTO DE ATENDIMENTO'
                    if unidade == '(UNIDADE BASICA DE SAUDE NELSON MACHADO DIAS)':
                        unidade = 'POSTO DE ATENDIMENTO'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA DR JOSE ISSA)':
                        unidade = 'JOSE ISSA'
                    if unidade == '(UNIDADE BASICA DE SAUDE DR JOSE ISSA)':
                        unidade = 'JOSE ISSA'
                    if unidade == '(UNIDADE BASICA DE SAUDE DR RODRIGO LIMA VILHANUEVA)':
                        unidade = 'KAMEL SAAD'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA JOSE ALBERTO VIEIRA BOCH)':
                        unidade = 'ESTORIL'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA JOSE ALBERTO F NEVES)':
                        unidade = 'ALEGRETE'
                    if unidade == '(UNIDADE BASICA DE SAUDE DA FAMILIA SANGA PUITA JOSE BATAGLIN)':
                        unidade = 'SANGA PUITA'
                    if unidade == '(UNIDADE BASICA DE SAUDE SANGA PUITA JOSE BATAGLIN)':
                        unidade = 'SANGA PUITA'
                    if unidade == '(UNIDADE BASICA DE SAUDE DR PEDRO MONTEIRO DE ALMEIDA)':
                        unidade = 'PEDRO MONTEIRO'
                    if unidade == '(UNIDADE DE SAUDE DA FAMILIA DR PEDRO MONTEIRO DE ALMEIDA)':
                        unidade = 'PEDRO MONTEIRO'
                    if unidade == '(CENTRO DE ESPECIALIDADE ODONTOLOGICA)':
                        unidade = 'CENTRAL DE REGULACAO DE PONTA PORA'
                        ceo_kayatt_nucleo = True
                    if unidade == '(LABORATORIO DE PROTESE DENTAL DE PONTA PORA)':
                        unidade = 'CENTRAL DE REGULACAO DE PONTA PORA'
                        ceo_kayatt_nucleo = True
                    
                    
                    #separando numero do telefone do ddd e verificando se telefone possui 9 digitos
                    quantidade_num = len(telefone)
                    print(quantidade_num)
                    if telefone != '-' and quantidade_num > 0:
                        ddd = telefone[:2]
                        telefone1 = telefone[2:]
                        quantidade_num = len(telefone1)
                        
                        if quantidade_num < 9:
                            telefone1 = '9'+telefone1
                    else:
                        ddd = '67'
                        telefone1 = '999999999'

                    #trocar por codigo especialidades
                    if espe_ou_proced == 'PROCEDIMENTOS':
                        especialidade = especialidade.replace("- ", "")
                    else: 
                        if especialidade == 'CONSULTA EM PSICOLOGIA':
                            especialidade1 = '999909'
                        elif especialidade == 'CONSULTA EM NUTRIÇÃO':
                            especialidade1 = '999906'
                        elif especialidade == 'CONSULTA EM CARDIOLOGIA':
                            especialidade1 = '225120'
                        elif especialidade == 'CONSULTA EM ANGIOLOGIA':
                            especialidade1 = '225115'
                        elif especialidade == 'CONSULTA EM CIRURGIA GERAL':
                            especialidade1 = '225225'
                        elif especialidade == 'CONSULTA EM DERMATOLOGIA':
                            especialidade1 = '225135'
                        elif especialidade == 'CONSULTA EM GINECOLOGIA':
                            especialidade1 = '999913'
                        elif especialidade == 'CONSULTA EM GINECOLOGIA E OBSTETRÍCIA':
                            especialidade1 = '225250'
                        elif especialidade == 'CONSULTA EM MASTOLOGIA':
                            especialidade1 = '225250'
                        elif especialidade == 'CONSULTA EM OTORRINOLARINGOLOGIA':
                            especialidade1 = '225275'
                        elif especialidade == 'CONSULTA EM NEFROLOGIA':
                            especialidade1 = '225109'
                        elif especialidade == 'CONSULTA EM OFTALMOLOGIA':
                            especialidade1 = '225265'
                        elif especialidade == 'CONSULTA EM OFTALMOLOGIA - PTERI':
                            especialidade1 = '225265'
                        elif especialidade == 'CONSULTA EM OFTALMOLOGIA - CATARATA':
                            especialidade1 = '225265'
                        elif especialidade == 'CONSULTA EM CIRURGIA BUCO-MAXILO FACIAL':
                            especialidade1 = '999921'
                        elif especialidade == 'CONSULTA EM ODONTOLOGIA - ENDODONTIA':
                            especialidade1 = '999917'
                        elif especialidade == 'CONSULTA EM REUMATOLOGIA':
                            especialidade1 = '225136'
                        elif especialidade == 'CONSULTA EM UROLOGIA':
                            especialidade1 = '225285'
                        elif especialidade == 'CONSULTA EM INFECTOLOGIA':
                            especialidade1 = '225103'
                        elif especialidade == 'CONSULTA EM ORTOPEDIA':
                            especialidade1 = '225270'
                        elif especialidade == 'CONSULTA EM ODONTOLOGIA - PRÓTESE DENTÁRIA':
                            especialidade1 = '999922'
                        elif especialidade == 'CONSULTA EM ODONTOLOGIA - PACIENTE COM NECESSIDADE ESPECIAL':
                            especialidade1 = '999922'
                        elif especialidade == 'CONSULTA EM ODONTOPEDIATRIA':
                            especialidade1 = '999922'
                        elif especialidade == 'CONSULTA EM ODONTOLOGIA - PERIODONTIA':
                            especialidade1 = '999919'
                        elif especialidade == 'CONSULTA EM FONOAUDIOLOGIA':
                            especialidade1 = '999904'
                        else:
                            if espe_ou_proced == 'ESPECIALIDADES':
                                nao_possui_procedimento = True
                            else:
                                nao_possui_procedimento = False
                                
                                                
                        


                    print(profissional1)
                    print(unidade)

                    #buscar numero do cid em site
                    if nao_possui_procedimento == False:
                        if cid == 'ESTADO DE INFECÇÃO ASSINTOMÁTICA PELO VÍRUS DA IMUNODEFICIÊNCIA HUMANA [HIV]':
                            cid = cid.replace(" [HIV]", "")
                      
                        while tentativa == True:
                            try:
                                
                                expect(pagina2.get_by_role("textbox", name="Busca CID")).to_be_visible(timeout=5000)
                                expect(pagina2.get_by_role("textbox", name="Busca CID")).to_be_enabled(timeout=5000)
                                pagina2.get_by_role("textbox", name="Busca CID").fill(cid)
                                
                                elemento = pagina2.locator('xpath=/html/body/main/section[1]/div[2]/astro-island/div/div[2]/div[2]/a[1]/span[2]').wait_for(timeout=5000)
                                cid_numero = pagina2.locator('xpath=/html/body/main/section[1]/div[2]/astro-island/div/div[2]/div[2]/a[1]/span[2]').text_content()
                                cid_numero = cid_numero.replace(".", "")
                            
                                print(cid_numero)

                                print('\n----------------------------------------------------')
                                
                                break
                        
                            except TimeoutError:
                                pagina2.reload()
                                
                        #adicionando novo encaminhamento
                        while tentativa == True:
                            try:
                                elemento = pagina1.locator('xpath=/html/body/div/aside/section/ul/li[7]/a').wait_for(timeout=60000)
                                pagina1.locator('xpath=/html/body/div/aside/section/ul/li[7]/a').click()
                                break
                            except TimeoutError:
                                pagina1.reload()

                        #buscando usuario
                        pagina1.get_by_role("link", name=" Novo").click()
                        while tentativa == True:
                            try:
                                time.sleep(2)
                                expect(pagina1.get_by_role("textbox", name="CNS *")).to_be_visible(timeout=60000)
                                expect(pagina1.get_by_role("textbox", name="CNS *")).to_be_enabled(timeout=60000)
                                pagina1.type("#duosystem_regulacaobundle_atendimentotransicao_paciente_cns",sus)

                                pagina1.locator('xpath=/html/body/div/div[1]/section[2]/div[1]/div[1]/form/div[2]/fieldset[1]/div[2]/div[4]/div/a[1]').click()

                                #fazer verificacao se o paciente é o mesmo do esaude
                                elemento = pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[4]').wait_for(timeout=10000)
                                nome_verificar = pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[4]').text_content()
                                print('Nome do paciente no esaude: '+paciente)
                                print('Nome do paciente no core: '+nome_verificar)
                                break
                            except TimeoutError:
                                pagina1.reload()
                        
                        if nome_verificar == paciente or nome_repitido == 1:
                            nome_repitido = 0
                            tentativa_verficar_paciente = 0
                            expect(pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[9]')).to_be_visible(timeout=60000)
                            expect(pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[9]')).to_be_enabled(timeout=60000)
                            cidade = pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[9]').text_content()

                            expect(pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[25]')).to_be_visible(timeout=60000)
                            expect(pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[25]')).to_be_enabled(timeout=60000)
                            pais = pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[25]').text_content()
                            
                            if cidade == 'PONTA PORA' or pais == 'PARAGUAI':

                                if idade < 17:
                                    mae = pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[6]').text_content()
                                    
                                
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[1]/input').click()
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[3]/button[1]').click()

                                if idade < 17:
                                    pagina1.get_by_role("textbox", name="Nome do(a) Responsável *").fill(mae)
                                    pagina1.type("#duosystem_regulacaobundle_atendimentotransicao_paciente_telefoneResponsavel",ddd+telefone1)
                                
                                if pais == 'PARAGUAI':

                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_cep")).to_be_visible(timeout=60000)
                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_cep")).to_be_enabled(timeout=60000)
                                    pagina1.type("#duosystem_regulacaobundle_atendimentotransicao_endereco_cep",'79904718')

                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_numero")).to_be_visible(timeout=60000)
                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_numero")).to_be_enabled(timeout=60000)
                                    pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_numero").click()
                                    pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_endereco_numero").fill('S/N')

                                expect(pagina1.locator("select#duosystem_regulacaobundle_atendimentotransicao_telefone_0_tipo")).to_be_visible(timeout=60000)
                                expect(pagina1.locator("select#duosystem_regulacaobundle_atendimentotransicao_telefone_0_tipo")).to_be_enabled(timeout=60000)
                                pagina1.select_option("select#duosystem_regulacaobundle_atendimentotransicao_telefone_0_tipo", "CEL")

                                expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_ddd")).to_be_visible(timeout=60000)
                                expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_ddd")).to_be_enabled(timeout=60000)
                                pagina1.type("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_ddd",ddd)

                                expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_ddd")).to_be_visible(timeout=60000)
                                expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_ddd")).to_be_enabled(timeout=60000)
                                pagina1.type("#duosystem_regulacaobundle_atendimentotransicao_telefone_0_numero",telefone1)

                                expect(pagina1.get_by_role("menuitem", name="Próximo")).to_be_visible(timeout=60000)
                                expect(pagina1.get_by_role("menuitem", name="Próximo")).to_be_enabled(timeout=60000)
                                time.sleep(2)
                                pagina1.get_by_role("menuitem", name="Próximo").click()

                                #selecionando unidade, profissional e cid
                                expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_unidadeServico')).to_be_visible(timeout=60000)
                                expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_unidadeServico')).to_be_enabled(timeout=60000)
                                pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_unidadeServico').click()
                                pagina1.type("#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_unidadeServico",unidade)

                                expect(pagina1.locator('#select2-results-29 .select2-result-label')).to_be_visible(timeout=60000)
                                expect(pagina1.locator('#select2-results-29 .select2-result-label')).to_be_enabled(timeout=60000)
                                pagina1.locator('#select2-results-29').click()
                                encontrou_medico = True
                                try:
                                    expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_profissional')).to_be_visible(timeout=60000)
                                    expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_profissional')).to_be_enabled(timeout=60000)
                                    pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_profissional').click()
                                    pagina1.type("#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_profissional",profissional1)

                                    elemento = pagina1.locator('#select2-results-31 .select2-result-label').wait_for(timeout=5000)
                                    pagina1.locator('#select2-results-31').click()
                                except TimeoutError:
                                    encontrou_medico = False
                                if encontrou_medico == True:
                                    expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_cid')).to_be_visible(timeout=60000)
                                    expect(pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_cid')).to_be_enabled(timeout=60000)
                                    pagina1.locator('#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_cid').click()
                                    pagina1.type("#s2id_duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_cid",cid_numero)
                                
                                    expect(pagina1.locator('#select2-results-37 .select2-result-label').first).to_be_visible(timeout=60000)
                                    expect(pagina1.locator('#select2-results-37 .select2-result-label').first).to_be_enabled(timeout=60000)
                                    pagina1.locator('#select2-results-37 .select2-result-label').first.click()   
                                    
                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_tipoCid")).to_be_visible(timeout=60000)
                                    expect(pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_tipoCid")).to_be_enabled(timeout=60000)
                                    pagina1.locator("#duosystem_regulacaobundle_atendimentotransicao_atendimento_atendimentoCid_0_tipoCid").select_option("0")

                                    expect(pagina1.get_by_role("menuitem", name="Próximo")).to_be_visible(timeout=60000)
                                    expect(pagina1.get_by_role("menuitem", name="Próximo")).to_be_enabled(timeout=60000)
                                    pagina1.get_by_role("menuitem", name="Próximo").click()

                                    #pagina.pause()
                                    #selecionar especialidade ou procedimantos
                                    if espe_ou_proced == 'PROCEDIMENTOS':
                                        expect(pagina1.locator('#s2id_pesquisa_procedimento')).to_be_visible(timeout=60000)
                                        expect(pagina1.locator('#s2id_pesquisa_procedimento')).to_be_enabled(timeout=60000)
                                        pagina1.locator('#s2id_pesquisa_procedimento').click()
                                        pagina1.type("#s2id_pesquisa_procedimento",especialidade)

                                        expect(pagina1.locator('#select2-results-41 .select2-result-label')).to_be_visible(timeout=60000)
                                        expect(pagina1.locator('#select2-results-41 .select2-result-label')).to_be_enabled(timeout=60000)
                                        pagina1.locator('#select2-results-41 .select2-result-label').click()
                                    else:
                                        expect(pagina1.locator('#s2id_pesquisa_especialidade')).to_be_visible(timeout=60000)
                                        expect(pagina1.locator('#s2id_pesquisa_especialidade')).to_be_enabled(timeout=60000)
                                        pagina1.locator('#s2id_pesquisa_especialidade').click()
                                        pagina1.type("#s2id_pesquisa_especialidade",especialidade1)

                                        expect(pagina1.locator('#select2-results-39 .select2-result-label')).to_be_visible(timeout=60000)
                                        expect(pagina1.locator('#select2-results-39 .select2-result-label')).to_be_enabled(timeout=60000)
                                        pagina1.locator('#select2-results-39 .select2-result-label').click()

                                    expect(pagina1.get_by_role("button", name=" Pesquisar")).to_be_visible(timeout=60000)
                                    expect(pagina1.get_by_role("button", name=" Pesquisar")).to_be_enabled(timeout=60000)
                                    pagina1.get_by_role("button", name=" Pesquisar").click()
                                
                                    if especialidade == 'CONSULTA EM ODONTOLOGIA - PRÓTESE DENTÁRIA':            
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_visible(timeout=60000)
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_enabled(timeout=60000)
                                        pagina1.select_option("select#subespecialidade_999922_0301010048_2", "PROTESE DENTARIA")
                                    if especialidade == 'CONSULTA EM ODONTOLOGIA - PACIENTE COM NECESSIDADE ESPECIAL':            
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_visible(timeout=60000)
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_enabled(timeout=60000)
                                        pagina1.select_option("select#subespecialidade_999922_0301010048_2", "portador de necessidades especiais (PNE)")
                                    if especialidade == 'CONSULTA EM ODONTOPEDIATRIA':            
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_visible(timeout=60000)
                                        expect(pagina1.locator("select#subespecialidade_999922_0301010048_2")).to_be_enabled(timeout=60000)
                                        pagina1.select_option("select#subespecialidade_999922_0301010048_2", "PEDIATRICa")
                                                            
                                    expect(pagina1.locator('xpath=/html/body/div[1]/div[1]/section[2]/div[1]/div[1]/form/div[2]/fieldset[3]/div[2]/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/input')).to_be_visible(timeout=5000)
                                    expect(pagina1.locator("xpath=/html/body/div[1]/div[1]/section[2]/div[1]/div[1]/form/div[2]/fieldset[3]/div[2]/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/input")).to_be_enabled(timeout=5000)
                                    pagina1.locator('xpath=/html/body/div[1]/div[1]/section[2]/div[1]/div[1]/form/div[2]/fieldset[3]/div[2]/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/input').click()
                                    if(especialidade.count("TOMOGRAFIA")) or (especialidade.count("RADIOGRAFIA")):
                                        messagebox.showinfo("Checkbox", "Adicione informacao desejada")
                                   
                                    try:
                                        elemento = pagina1.get_by_role("button", name="Salvar").wait_for(timeout=5000)
                                        pagina1.get_by_role("button", name="Salvar").click()

                                        elemento = pagina1.get_by_role("menuitem", name="Próximo").wait_for(timeout=5000)
                                        pagina1.get_by_role("menuitem", name="Próximo").click()
                                        try:
                                            #ultimo passo verificar dados do paciente e colocar quadro clinico
                                            elemento = pagina1.locator('#resumo_paciente_nome').wait_for(timeout=5000)
                                            nome_do_paciente = pagina1.locator('#resumo_paciente_nome').text_content()
                                            print(nome_do_paciente)

                                            expect(pagina1.locator('#resumo_atendimento_profissional')).to_be_visible(timeout=60000)
                                            expect(pagina1.locator('#resumo_atendimento_profissional')).to_be_enabled(timeout=60000)
                                            crm_medico = pagina1.locator('#resumo_atendimento_profissional').text_content()


                                            verificar = pagina.locator(".col-md-12 > div:nth-child(3)").first.text_content()
                                            quadro_clinico = verificar.replace("Avaliação/Justificativa: ", "")
                                            quadro_clinico = quadro_clinico.replace(" Motivo/Quadro:", "")
                                            quadro_clinico = quadro_clinico.replace("Observação", ".")

                                            if ceo_kayatt_nucleo == True:
                                                expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_visible(timeout=60000)
                                                expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_enabled(timeout=60000)
                                                pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao').fill('Em consulta com Dr(a) '+crm_medico+' no dia '+data_retorno+' onde o mesmo solicita retorno de '+dias_retorno+'. '+quadro_clinico+'. esaude')
                                                #cont = cont+1
                                                #tentativa_verficar_paciente = 0
                                            else:
                                                if telemedicina == True:
                                                    expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_visible(timeout=60000)
                                                    expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_enabled(timeout=60000)
                                                    pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao').fill('Em consulta pela telemedicina onde Dr(a) '+crm_medico+' transcreve pedido para '+especialidade+'.'+quadro_clinico+'esaude')
                                                else:
                                                    expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_visible(timeout=60000)
                                                    expect(pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao')).to_be_enabled(timeout=60000)
                                                    pagina1.locator('#duosystem_regulacaobundle_fichaapacpadrao_observacao').fill('Em consulta com Dr(a) '+crm_medico+' onde o mesmo encaminha para '+especialidade+'.'+quadro_clinico+'esaude')
                                                #cont = cont+1
                                                #tentativa_verficar_paciente = 0
                                            estado = var_checkbox.get()
                                            if estado == 1:
                                                
                                                messagebox.showinfo("Checkbox", "Ficha lançada\nVerifique antes de prosseguir")
                                                '''
                                                expect(pagina.locator('#concluido').click()).to_be_visible(timeout=60000)
                                                expect(pagina.locator('#concluido').click()).to_be_enabled(timeout=60000)
                                                pagina.locator('#concluido').click()

                                                time.sleep(2)

                                                expect(pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[9]/form/div[2]/div/button')).to_be_visible(timeout=5000)
                                                expect(pagina.locator("xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[9]/form/div[2]/div/button")).to_be_enabled(timeout=5000)
                                                pagina.locator('xpath=/html/body/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[9]/form/div[2]/div/button').click()
                                                '''
 
                                            else:
                                                cont = cont+1
                                                print(quadro_clinico)
                                        except TimeoutError:
                                            pagina1.reload()
                                            cont = cont+1
                                            tentativa_verficar_paciente = 0  
                                    except:
                                        pagina1.reload()
                                        cont = cont+1
                                        tentativa_verficar_paciente = 0 
                                else:
                                    pagina1.reload()
                                    cont = cont+1
                                    tentativa_verficar_paciente = 0
                                    

                            else:
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[1]/input').click()
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[3]/button[1]').click()
                                cont = cont+1
                                tentativa_verficar_paciente = 0
                        else:
                            
                            if tentativa_verficar_paciente < 1:
                                nome_repitido = simpledialog.askinteger("Entrada", "Paciente correto?")
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[1]/input').click()
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[3]/button[1]').click()
                                tentativa_verficar_paciente = tentativa_verficar_paciente + 1
                            else:
                                cont = cont+1
                                tentativa_verficar_paciente = 0
                                print('paciente nao possui o mesmo nome: '+nome_verificar+' --------- '+paciente)
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[2]/table/tbody/tr/td[1]/input').click()
                                pagina1.locator('xpath=/html/body/div[1]/div[6]/div/div/div[3]/button[1]').click()
                    else:
                        cont = cont + 1
                else:
                    cont = cont+1
            else:
                cont = cont+1
                
     
            
            
            pagina2.get_by_role("link", name="cid.api.br").click()
            try:
                elemento = pagina.get_by_role("link", name="Regulação").wait_for(timeout=5000)
                pagina.get_by_role("link", name="Regulação").click()
            except:
                pagina.reload()
           
       



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
