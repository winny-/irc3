# -*- coding: utf-8 -*-
from irc3 import testing


class TestCommands(testing.ServerTestCase):

    def test_not_registered(self):
        s = self.callFTU(clients=3, opers={'superman': 'passwd'})
        del s.client1.data['nick']
        s.client1.dispatch('OPER superman passwd')
        self.assertSent(
            s.client1, ':irc.com 451 None :You have not registered')

    def test_die(self):
        s = self.callFTU(clients=3, opers={'superman': 'passwd'})
        s.client1.dispatch('OPER superman passwd')
        s.client1.dispatch('DIE')

    def test_oper(self):
        s = self.callFTU(clients=3, opers={'superman': 'passwd'})
        s.client2.modes.add('w')
        s.client1.dispatch('OPER c c')
        self.assertSent(s.client1, ':irc.com 464 client1 :Password incorrect')

        s.client1.dispatch('WALLOPS Hi!')
        self.assertSent(
            s.client1,
            (':irc.com 481 client1 '
             ':Permission Denied- You\'re not an IRC operator'))

        s.client1.dispatch('OPER superman passwd')
        self.assertSent(
            s.client1, ':irc.com 381 client1 :You are now an IRC operator')

        s.client1.dispatch('WALLOPS Hi!')
        self.assertSent(
            s.client2, ':client1!uclient1@127.0.0.1 NOTICE client2 :Hi!')
        self.assertNotSent(
            s.client3, ':client1!uclient1@127.0.0.1 NOTICE client3 :Hi!')