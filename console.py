#!/usr/bin/python3
"""
Program that contain the entry point of the command interpreter
"""

import shlex
import cmd
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter """
    prompt = "(hbnb) "

    all_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        """Ignor empty spaces"""
        pass

    def do_quit(self, arg):
        """Quit command"""
        return True

    def do_EOF(self, arg):
        """Quit command to exit at end of file"""
        return True

    def help_quit(self):
        """Quit command"""
        print("Quit command to exit the program\n")

    def help_EOF(self):
        """EOF command to quit"""
        print("EOF command to exit the program\n")

    def do_create(self, arg):
        """Creates a new instance of basemodel"""
        try:
            if not arg:
                raise SyntaxError()
            _list = arg.split(" ")
            obj = eval("{}()".format(_list[0]))
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name mising **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Print the str of an instance"""
        _line = shlex.split(arg)
        if len(_line) == 0:
            print("** class name missing **")
        elif _line[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(_line) == 1:
            print("** instance id missing **")
        elif len(_line) == 2:
            key = _line[0] + "." + _line[1]
            ob = storage.all()
            if ob.get(key):
                print(ob[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance"""
        try:
            if not arg:
                raise SyntaxError()
            _list = arg.split(" ")
            if len(_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = _list[0] + '.' + _list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, arg):
        """Print all str of all instances"""
        objects = storage.all()
        _list = []
        if arg:
            if arg in self.all_classes:
                for key, v in objects.items():
                    splitkey = key.split(".")
                    if splitkey[0] == arg:
                        _list.append(str(v))
            else:
                print("** class doesn't exist **")
        else:
            for v in objects.values():
                _list.append(str(v))

        if _list != []:
            print(_list)

    def do_update(self, arg):
        """Adding or updating attributes"""
        _line = shlex.split(arg)
        if len(_line) == 0:
            print("** class name missing **")
        elif _line[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(_line) == 1:
            print("** instance id missing **")
        elif len(_line) == 2:
            if storage.all().get(_line[0] + "." + _line[1]):
                print("** attribute name missing **")
            else:
                print("** no instance found **")
        elif len(_line) == 3:
            print("** value missing **")
        else:
            if _line[0] in self.all_classes:
                key = _line[0] + "." + _line[1]
                objects = storage.all()
                if key in objects:
                    value = objects.get(key)
                    try:
                        attr = getattr(value, _line[2])
                        setattr(value, _line[2], type(attr)(_line[3]))
                    except:
                        setattr(value, _line[2], _line[3])
                    storage.save()
                else:
                    print("** no instance found **")


"""Interactive or no interactive mode"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()
