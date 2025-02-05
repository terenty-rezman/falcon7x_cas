import all_messages

# словарь со всеми полученными сообщениями
all_recieved_mssgs = {
    
}
current_regime = 'cruise' # текущий режима
display_mssgs  = list() # все сообщения, которые нужно отобразить
recieved_red = list() # полученные красные сообщения
recieved_amber = list() # полученные желтые сообщения
recieved_white = list() # полученные белые сообщения
visible_mssgs = list() # сообщения, которые в данный момент находятся на экране
amber_and_white_mssgs = list()
end_mssg = 'END' #  самое последнее сообщение
scroll_index = 0 # индекс для прокрутки
final_mssgs_list = [None]*10
# final_mssgs_list.insert(0, 'END')

recieved_amber_not_read = list() 
recieved_amber_read = list()

amber_count_up = 0
white_count_up = 0
amber_count_down = 0
white_count_down = 0


# функция для добавления пришедшего сообщения в общий список и сортировки его по цвету
def add_mssg(msg_text):

    if msg_text in all_recieved_mssgs:
        return

    msg_cls: all_messages.CASmssg = all_messages.all_mssgs[msg_text]

    # msg_cls.is_read = False
    all_recieved_mssgs[msg_text] = msg_cls # добавление класса с сообщением в словарь: ключ - текст сообщения, значение - его класс
    
    all_recieved_mssgs_values = list(all_recieved_mssgs.values()) # получение классов из словаря
    

    # сортировка последнего полученного сообщения (если пришедшее сообщение добавляется в начало списка)
    if all_recieved_mssgs_values[-1].color == 'R':
        recieved_red.insert(0, all_recieved_mssgs_values[-1])
    elif all_recieved_mssgs_values[-1].color == 'A':
        recieved_amber.insert(0, all_recieved_mssgs_values[-1])
    else:
        recieved_white.insert(0, all_recieved_mssgs_values[-1])
    
    
    # список всех отсортированных сообщений
    global display_mssgs
    global visible_mssgs
    display_mssgs = recieved_red + recieved_amber + recieved_white
    visible_mssgs = display_mssgs[:]

    final_result()

    return msg_cls.color

    


def scroll_for_1_message(scroll_for_one_mssg_bttn_down, scroll_for_one_mssg_bttn_up):
    global visible_mssgs
    global display_mssgs
    global scroll_index
    global recieved_amber_not_read
    global recieved_amber_read
    global amber_count_up
    global white_count_up
    global amber_count_down
    global white_count_down
    global amber_and_white_mssgs

    recieved_amber_not_read.clear()
    recieved_amber_read.clear()

    # # определяем непрочитанные желтые сообщения
    # for i in recieved_amber:
    #     if i.isread == False:
    #         recieved_amber_not_read.append(i)
    #     elif i.isread == True and getattr(i, current_regime) == True:
    #         recieved_amber_read.append(i)

    # amber_and_white_mssgs = recieved_amber_read + recieved_white # список всех желтых и белых сообщений

    if scroll_for_one_mssg_bttn_up == True and visible_mssgs[0:10] == display_mssgs[0:10]:
        pass   # выход из цикла, если мы в начале списка, т.к. индекс остался неизменным
    elif scroll_for_one_mssg_bttn_down == True and scroll_index == len(amber_and_white_mssgs):
        pass   # выход из цикла, если мы в конце списка, т.е. отображается только сообщение END
    elif scroll_for_one_mssg_bttn_down == True:
        scroll_index += 1
        visible_mssgs = recieved_red + recieved_amber_not_read + amber_and_white_mssgs[scroll_index:]
    elif scroll_for_one_mssg_bttn_up == True:
        scroll_index -= 1
        visible_mssgs = recieved_red + recieved_amber_not_read + amber_and_white_mssgs[scroll_index:]


    # # количество желтых и белых сообщений до отображаемых
    # for item in amber_and_white_mssgs[0:scroll_index]:
    #     if item.color == "A":
    #         amber_count_up += 1
    #     else:
    #         white_count_up += 1

    # # количество желтых и белых сообщений после отображаемых
    # for item in amber_and_white_mssgs[scroll_index + (10-len(recieved_red)-len(recieved_amber_not_read)):]: 
    #     if item.color == "A":
    #         amber_count_down += 1
    #     else:
    #         white_count_down += 1

    # if scroll_for_one_mssg_bttn_down == True:
    #     print('Прокрутка на одно сообщение вниз')
    # elif scroll_for_one_mssg_bttn_up == True:
    #     print('Прокрутка на одно сообщение вверх')
    
    final_result()

    # print(len(amber_and_white_mssgs))
    # print(scroll_index)


def reading_mssgs(bttn_to_read_mssgs):

    if bttn_to_read_mssgs == True: # если нажата кнопка прочтения сообщений
        for item_f in final_mssgs_list:
            if item_f != None:
                item_f.isread = True # меняем атрибут класса отображаемых сообщений на прочитано

        for item_d in display_mssgs: 
            if item_d == item_f: # если отображаемое сообщение совпадает с сообщением в списке всех сообщений
                item_d.isread = True # то также меняем и его атрибут
        
        for item_v in visible_mssgs: 
            if item_v == item_f: # если отображаемое сообщение совпадает с сообщением в списке всех сообщений
                item_v.isread = True # то также меняем и его атрибут

        for item_r in recieved_red: 
            if item_r == item_f: # если отображаемое сообщение совпадает с сообщением в списке полученных красных
                item_r.isread = True # то также меняем и его атрибут

        for item_a in recieved_amber: 
            if item_a == item_f: # если отображаемое сообщение совпадает с сообщением в списке полученных желтых
                item_a.isread = True # то также меняем и его атрибут
        
    

    # print('Прочтение сообщений')
    final_result()

# прочтение белых сообщений через 10 секунд


# функция для удаления сообщения
def remove_message(message_to_delete):
    global display_mssgs
    global visible_mssgs
    global recieved_red
    global recieved_amber
    global recieved_white

    # обновление списка полученных красных
    for item_r in recieved_red:
        if message_to_delete == item_r.text:
            recieved_red.remove(item_r)
    # обновление списка полученных желтых
    for item_a in recieved_amber:
        if message_to_delete == item_a.text:
            recieved_amber.remove(item_a)
    # обновление списка полученных белых
    for item_w in recieved_white:
        if message_to_delete == item_w.text:
            recieved_white.remove(item_w)
    
    # удаление сообщения в общем списке сообщений
    for item_d in display_mssgs:
        if message_to_delete == item_d.text:
            display_mssgs.remove(item_d)

    # удаление сообщения в отображаемом списке сообщений
    for item_v in visible_mssgs:
        if message_to_delete == item_v.text:
            visible_mssgs.remove(item_v)

    del all_recieved_mssgs[message_to_delete]
    
    final_result()

def remove_message(message_to_delete):
    global display_mssgs
    global visible_mssgs
    global recieved_red
    global recieved_amber
    global recieved_white

    # обновление списка полученных красных
    for item_r in recieved_red:
        if message_to_delete == item_r.text:
            recieved_red.remove(item_r)
    # обновление списка полученных желтых
    for item_a in recieved_amber:
        if message_to_delete == item_a.text:
            recieved_amber.remove(item_a)
    # обновление списка полученных белых
    for item_w in recieved_white:
        if message_to_delete == item_w.text:
            recieved_white.remove(item_w)
    
    # удаление сообщения в общем списке сообщений
    for item_d in display_mssgs:
        if message_to_delete == item_d.text:
            display_mssgs.remove(item_d)

    # удаление сообщения в отображаемом списке сообщений
    for item_v in visible_mssgs:
        if message_to_delete == item_v.text:
            visible_mssgs.remove(item_v)

    del all_recieved_mssgs[message_to_delete]
    
    final_result()

def remove_all_messages():
    global all_recieved_mssgs
    global display_mssgs
    global recieved_red
    global recieved_amber
    global recieved_white
    global visible_mssgs
    global amber_and_white_mssgs
    global scroll_index
    global final_mssgs_list

    # Очистка всех данных
    all_recieved_mssgs.clear()
    display_mssgs.clear()
    recieved_red.clear()
    recieved_amber.clear()
    recieved_white.clear()
    visible_mssgs.clear()
    amber_and_white_mssgs.clear()
    scroll_index = 0  # Сброс индекса прокрутки
    final_mssgs_list = [None] * 10  # Сброс итогового списка сообщений

    final_result()



def final_result():
    global final_mssgs_list
    global visible_mssgs
    global amber_count_up_str
    global amber_count_down_str
    global white_count_up_str
    global white_count_down_str

    global scroll_index
    global recieved_amber_not_read
    global recieved_amber_read
    global amber_count_up
    global white_count_up
    global amber_count_down
    global white_count_down
    global amber_and_white_mssgs

    final_mssgs_list = [None]*9
    final_mssgs_list.insert(0, 'END')

    k = 0
    
    for item in range(0, len(visible_mssgs)):
        if k > 9:
            break 
        elif getattr(visible_mssgs[item], current_regime) == True: 
            # final_mssgs_list[k] = visible_mssgs[item]
            final_mssgs_list.insert(k, visible_mssgs[item])
            k +=1
    
    if None in final_mssgs_list:
        index_none = final_mssgs_list.index(None)
        final_mssgs_list = final_mssgs_list[0:index_none]
    
    recieved_amber_not_read = list() 
    recieved_amber_read = list()
    all_amber_and_white_mssgs = list()

    # определяем непрочитанные желтые сообщения
    for i in recieved_amber:
        if i.isread == False and getattr(i, current_regime) == True:
            recieved_amber_not_read.append(i)
        elif i.isread == True and getattr(i, current_regime) == True:
            recieved_amber_read.append(i)

    amber_and_white_mssgs = recieved_amber_read + recieved_white # список всех прочитанных желтых и белых сообщений
    all_amber_and_white_mssgs = recieved_amber_not_read + amber_and_white_mssgs

    # print(len(recieved_red))
    # print(len(recieved_amber))
    # print(len(recieved_white))
    # print(len(recieved_amber_read))
    # print(len(recieved_amber_not_read))


    # счетчики сообщений сверху и снизу отображаемых
    amber_count_up = 0
    white_count_up = 0
    amber_count_down = 0
    white_count_down = 0

    # print(amber_and_white_mssgs[scroll_index + (10-len(recieved_red)-len(recieved_amber_not_read)):])

    # количество желтых и белых сообщений до отображаемых
    for item in amber_and_white_mssgs[0:scroll_index]:
        if item.color == "A":
            amber_count_up += 1
        else:
            white_count_up += 1

    # количество желтых и белых сообщений после отображаемых
    for item in amber_and_white_mssgs[scroll_index + (10-len(recieved_red)-len(recieved_amber_not_read)):]: 
        if item.color == "A":
            amber_count_down += 1
        else:
            white_count_down += 1

    # преобразование чисел в строку для вывода на экран
    if amber_count_up <= 9:
        amber_count_up_str = '0' + str(amber_count_up)
    else:
        amber_count_up_str = str(amber_count_up)
    
    if amber_count_down <= 9:
        amber_count_down_str = '0' + str(amber_count_down)
    else:
        amber_count_down_str = str(amber_count_down)
    
    if white_count_up <= 9:
        white_count_up_str = '0' + str(white_count_up)
    else:
        white_count_up_str = str(white_count_up)

    if white_count_down <= 9:
        white_count_down_str = '0' + str(white_count_down)
    else:
        white_count_down_str = str(white_count_down)

    # print(final_mssgs_list)
    # print(amber_count_down, white_count_down,amber_count_up,white_count_up)
    
    

    


## Проверка
final_result()
print(final_mssgs_list)


add_mssg("IRS 1+2+3 NO POS ENTRY") #W  cruise = True
add_mssg("AVC: AGM #+#+# FAIL") #A  cruise = True
add_mssg("90 PRESS: CABIN ALT TOO HI") #R cruise = True
add_mssg("AVC: ASCB FAULT") #A cruise = False
add_mssg("AVC: APM 1+2+3+4 FAIL") #A cruise = False
add_mssg("15 COND: AFT FCS BOX OVHT") #R cruise = True
add_mssg("AVC AURAL WARN 1+2 INHIBIT") #W cruise = True
add_mssg("30 ELEC: BAT 1 OVHT") #R cruise = True
add_mssg("AVC: VALIDATE CONFIG") #W cruise = True
add_mssg("AVC: GEN IO 1+2+3+4+5 FAIL") #A cruise = True
add_mssg("AVC: MAU 1A+1B HI TEMP") #A cruise = True
# add_mssg("HUMID: FAULT") #"W"
# add_mssg("31 ELEC: BAT 2 OVHT") #R
# add_mssg("32 ELEC: BAT 1+2 OVHT") #R
# add_mssg("BLEED: APU FAULT") #A
# add_mssg("WATER: AFT HEATER HI TEMP") #A
# add_mssg("APU: AUTO SHUTDOWN")#A
# add_mssg("DOOR: EMERG NOT SECURED") #A

print(final_mssgs_list)

# scroll_for_one_mssg_bttn_down = True # кнопка для прокрутки сообщений на 1 вниз
# scroll_for_one_mssg_bttn_up = False # кнопка для прокрутки сообщений на 1 вверх


# print('Прокрутка на два сообщения вниз и на одно вверх')
# scroll_for_1_message(scroll_for_one_mssg_bttn_down, scroll_for_one_mssg_bttn_up)
# scroll_for_1_message(True, scroll_for_one_mssg_bttn_up)
# scroll_for_1_message(False, True)


# print('Желтых сообщений до')
# print(amber_count_up)
# print('Белых сообщений до')
# print(white_count_up)
# print('Желтых сообщений после')
# print(amber_count_down)
# print('Белых сообщений после')
# print(white_count_down)

# bttn_to_read_mssgs = True

# reading_mssgs(bttn_to_read_mssgs)


# scroll_for_1_message(True, False)
# scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# # scroll_for_1_message(True, False)
# scroll_for_1_message(False, True)
# scroll_for_1_message(False, True)



# add_mssg("AVC: GEN IO 1+2+3+4+5 FAIL") #A cruise = True
# add_mssg("DOOR: PAX NOT SECURED") #A cruise = True

# # Удаление сообщения
# message_to_delete = "IRS 1+2+3 NO POS ENTRY"
# remove_message(message_to_delete)

# print(final_mssgs_list)

# add_mssg("IRS 1+2+3 NO POS ENTRY") #W  cruise = True

remove_all_messages()
print(final_mssgs_list)