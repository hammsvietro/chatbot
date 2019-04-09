import telebot
from telebot import types

token = "879004433:AAElv3abIUlaEa_1jtUZNyCVb2YW8GDGT0I"
pidrow = telebot.TeleBot(token)

# Begin Usuario
class Usuario:

  def __init__(self, id):
    self.id = id
    
  def getId(self):
    return self.id

  def setNome(self, nome):
    self.nome = nome

  def setIdade(self, idade):
    self.idade = idade
  
  def setSexo(self, sexo):
    self.sexo = sexo

  def setAltura(self, altura):
    self.altura = altura

  def setEmail(self, email):
    self.email = email

  def getNome(self):
    return self.nome

  def printlist(self):
    msg = '\nID Telegram: {}\nNome: {}\nIdade: {} anos\nSexo: {}\nAltura: {}m\nEmail: {}'.format(self.id, self.nome, self.idade, self.sexo, self.altura, self.email)
    return msg


# End Usuario


def isCadastrado(lista, id):
  for elem in lista:
    if elem.getId() == id:
      return True
  return False

cadastrados = []

# CallBack Start
@pidrow.message_handler(commands=['start'])
def iniciodarodada(message):

  pidrow.send_message(message.chat.id,"Bem Vindo!\nDigite /help para saber os comandos")

# CallBack Help
@pidrow.message_handler(commands=['help'])
def help(message):
  pidrow.send_message(message.chat.id,'/cadastrar: Cadastrar novo usuario\n/listar: Lista usuarios ja cadastrados\n/deletar: deleta seu proprio usuario')

# CallBack Cadastrar
@pidrow.message_handler(commands=['cadastrar'])
def cadastrar(message):
  if isCadastrado(cadastrados, message.chat.id):
    pidrow.send_message(message.chat.id,"ID ja utilizada")
    return

  pedro = Usuario(message.chat.id)

  def confirmarCadastro(message):
    if message.text.lower() == 'sim':
      cadastrados.append(pedro)
      pidrow.send_message(message.chat.id, 'Cadastro efetuado com sucesso!')
    else:
      pidrow.send_message(message.chat.id, 'Para efetuar um novo cadastro digite /cadastrar')  

  def lerEmail(message):
    pedro.setEmail(message.text)
    msg = pidrow.send_message(message.chat.id, 'Obrigado, confirme seus dados por favor' + pedro.printlist()+"\nCaso tudo esteja ok, responda com Sim")
    pidrow.register_next_step_handler(msg, confirmarCadastro)

  def lerAltura(message):
    try:
      pedro.setAltura(float(message.text))
      msg = pidrow.send_message(message.chat.id, 'Qual o seu e-mail?')
      pidrow.register_next_step_handler(msg, lerEmail)
    except:
      msg = pidrow.send_message(message.chat.id, 'Ops, nao entendi sua resposta! estava esperando um numero.\n\
                                                  Certifique que voce usou um ponto para separar os decimais\nQual a sua altura?')
      pidrow.register_next_step_handler(msg,lerAltura)

  def lerSexo(message):
    pedro.setSexo(message.text)
    msg = pidrow.send_message(message.chat.id, 'Qual a sua altura?')
    pidrow.register_next_step_handler(msg, lerAltura)

  def lerIdade(message):
    try:
      idade = int(message.text)
      pedro.setIdade(idade)
      msg = pidrow.send_message(message.chat.id, 'Qual o seu sexo?')
      pidrow.register_next_step_handler(msg, lerSexo)
    except:
      msg = pidrow.send_message(message.chat.id, 'Ops, nao entendi sua resposta! estava esperando um numero\
                                                  \nQual o sua idade?')
      pidrow.register_next_step_handler(msg, lerIdade)

  def lerNome(message):
    pedro.setNome(message.text)
    msg = pidrow.send_message(message.chat.id, 'Ola {}, qual a sua idade?'.format(pedro.getNome()))
    pidrow.register_next_step_handler(msg, lerIdade)

  markup = types.ReplyKeyboardRemove(selective=False)

  msg = pidrow.send_message(message.chat.id, 'Qual o seu nome?', reply_markup=markup)
  pidrow.register_next_step_handler(msg, lerNome)

# CallBack listar
@pidrow.message_handler(commands=['listar'])
def listar(message):
  for usuario in cadastrados:
    pidrow.send_message(message.chat.id, usuario.printlist())
#CallBack Deletar
@pidrow.message_handler(commands=['deletar'])
def deletar(message):


  for user in cadastrados:
    if int(user.getId()) == int(message.chat.id):
        cadastrados.remove(user)
        pidrow.send_message(message.chat.id,'Usuario deletado com sucesso')
        return
    pidrow.send_message(message.chat.id,'ID nao encontrado nos usuarios cadastrados')
    return
  
  
  

pidrow.polling()
