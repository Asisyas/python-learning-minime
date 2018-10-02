
import minime.bot.service.brain.brain as bb
import minime.bot.service.session.session_factory as ss
import minime.bot.model.class_user as u



import minime.modules.git.provider.class_gitlab as GL

sf = ss.get_default()
usr = u.User()

usr.id = 'stanislau_komar'
usr.name = 'Stanislau Komar'

session = sf.create(usr)
brain = bb.Bot_Brain()




gl = GL.Gitlab_Provider('test', 'https://git.epam.com', 'email', email='stanislau_komar@epam.com', password='1319Vasilevich')
gl.get_projects()


#while True:
#    s = input()

#    if s == 'exit':
#        break

#    print(brain.response(s, session))
#    print("--------------")