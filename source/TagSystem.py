# class to manage all the tags in the cook book or a particular recipe
class TagSystem:
   
    def __init__(self, tags = None):
        #self.tag_list is always sorted
        if tags:
            self.tag_list = sorted(list(dict.fromkeys(tags)))
        else:
            self.tag_list = [] 
       
    def create_tag(self, new_tag: str):
        if new_tag not in self.tag_list:
            self.tag_list.append(new_tag)
            self.tag_list.sort()

    def set_tags(self, tags):
        self.tags = sorted(list(dict.fromkeys(tags)))
        
    def remove_tag(self, tag: str):
        self.tag_list.remove(tag)

    def clear(self):
        self.tag_list.clear()

    def get_tags(self, filter_func = None):
        if filter_func:
            return list(filter(filter_func, self.tag_list))
        else:
            return self.tag_list    

    def __str__(self):
        return ' '.join(self.tag_list)

    