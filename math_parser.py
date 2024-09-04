import re

# ↓ INFO NECESARIA PARA EL PARSER ↓
greek_letters = {
    'varepsilon': 'ϵ', 
    'vartheta': 'ϑ', 
    'epsilon': 'ε', 
    'upsilon': 'υ', 
    'Upsilon': 'Υ', 
    'lambda': 'λ', 
    'Lambda': 'Λ', 
    'varrho': 'ϱ', 
    'varphi': 'ϕ', 
    'alpha': 'α', 
    'gamma': 'γ', 
    'Gamma': 'Γ', 
    'delta': 'δ', 
    'Delta': 'Δ', 
    'theta': 'θ', 
    'Theta': 'Θ', 
    'kappa': 'ϰ', 
    'sigma': 'σ', 
    'Sigma': 'Σ', 
    'omega': 'ω', 
    'Omega': 'Ω', 
    'beta': 'β', 
    'zeta': 'ζ', 
    'iota': 'ι', 
    'eta': 'η', 
    'rho': 'ρ', 
    'tau': 'τ', 
    'phi': 'φ', 
    'Phi': 'Φ', 
    'chi': 'χ', 
    'psi': 'ψ', 
    'Psi': 'Ψ', 
    'mu': 'μ', 
    'nu': 'ν', 
    'xi': 'ξ', 
    'pi': 'π', 
    'Pi': 'Π'
}

arrows = {
    'rightleftharpoons': '↔', 
    'rightharpoondown': '←', 
    'leftharpoondown': '→', 
    'leftrightarrow': '↔', 
    'Leftrightarrow': '↔', 
    'rightharpoonup': '←', 
    'leftharpoonup': '→', 
    'Updownarrow': '↕', 
    'rightarrow': '←', 
    'Rightarrow': '←', 
    'longmapsto': 
    'longmapsto', 
    'leftarrow': '→', 
    'Leftarrow': '→', 
    'downarrow': '↓', 
    'Downarrow': '↓', 
    'uparrow': '↑', 
    'Uparrow': '↑', 
    'nearrow': ' -nearrow- ', 
    'searrow': ' -searrow- ', 
    'swarrow': ' -swarrow- ', 
    'nwarrow': ' -nwarrow- ', 
    'mapsto': '-mapsto- '
}

hats = {
    r"hat {a}": "â",
    r"hat {e}": "ê",
    r"hat {i}": "î",
    r"hat {o}": "ô",
    r"hat {u}": "û",
    r"hat": ""
}

miscellaneous = {
    'blacksquare': '■', 
    'varnothing': '∅', 
    'complement': '∁', 
    'emptyset': '∅', 
    'triangle': '△', 
    'partial': '∂', 
    'nexists': '∄', 
    'forall': '∀', 
    'exists': '∃', 
    'square': '□', 
    'infty': '∞', 
    'nabla': '∇', 
    'cdots': '…', 
    'surd': '√', 
    'neg': '¬', 
    'Re': 'R', 
    'Im': 'I', 
    'wp': '℘'
} 

relation_symbols = {
    'boxtimes': '⛝', 
    'subset': '⊂', 
    'approx': '≈', 
    'otimes': '⊗', 
    'times': '×', 
    'notin': '∉', 
    'simeq': '≃', 
    'wedge': '∧', 
    'oplus': '⊕', 
    'equiv': '≡', 
    'cdot': '⋅', 
    'perp': '⟂', 
    'cong': '≅', 
    'div': '÷', 
    'cap': '∩', 
    'cup': '∪', 
    'neq': '≠', 
    'leq': '≤', 
    'geq': '≥', 
    'vee': '∨', 
    'Box': '□', 
    'in': '⋹'
}

def sort_dict (dict):
    def dict_key (letter):
        return len(letter)
    
    dict_keys = [*dict.keys()]
    dict_keys.sort(key=dict_key, reverse=True)
    dict_values = [dict[x] for x in dict_keys]

    new_dict = {}

    for i in range(len(dict_keys)):
        key = dict_keys[i]
        value = dict_values[i]
        new_dict[key] = value
    
    print(new_dict)

# ↑ INFO NECESARIA PARA EL PARSER ↑

class MatrixObj:
    def __init__(self, common_string, op="{", cl="}", r=0):
        self.__ref = []
        self.last_level = 0
        self.__modules = []
        self.__common_string = common_string

        nested = self.setNestedData(common_string, op, cl, r)
        def key (x):
            return x["level"]
    
        nested.sort(key=key, reverse=True)
    
        self.addModules([NestedObj(x["content"], x["level"], self) for x in nested], common_string)

    def setNestedData(self, string, open_s="{", close_s="}", relative=0):
        wait_for_close = []
        nested_data = []
        level_counter = 0

        for i in range(len(string)):
            if (string[i] == open_s):
                wait_for_close.append([i, level_counter + relative])
                level_counter += 1
            elif (string[i] == close_s):
                last_element = wait_for_close.pop()
                state = {
                    "content": [last_element[0], i + 1],
                    "level": last_element[1]
                }
                level_counter -= 1
                nested_data.append(state)

        def key (x):
            return x["level"]
    
        nested_data.sort(key=key, reverse=True)
        self.last_level = nested_data[0]["level"]
        self.__common_string = string
        self.__ref = nested_data
        return nested_data
    
    def getNestedData(self):
        return self.__ref

    def _updateStructure(self, common_string):
        nested = self.setNestedData(common_string)
        def key (x):
            return x["level"]
        nested.sort(key=key, reverse=True)

        self.__modules = []
    
        self.addModules([NestedObj(x["content"], x["level"], self) for x in nested], common_string)
     
    def replaceModule(self, new_module, level, l_index):
        com = self.__common_string
        m = self.getModule(level, l_index)
        cl = m.range[1]

        #print("COMMON: " + com)
        #print("OLD MODULE: " + com[m.range[0]:m.range[1]], "\nRANGE: ", m.range)
        #print("NEW MODULE: " + new_module.getText(), "\nRANGE: ", [m.range[0], m.range[0] + tl])
        #print("NEW COMMON: " + com[0:m.range[0]] + new_module.getText() + com[cl:])
        new_com = com[0:m.range[0]] + new_module.getText() + com[cl:]

        self._updateStructure(new_com)

    def getCommon(self):
        return self.__common_string

    def removeModule(self, level, l_index):
        com = self.__common_string
        m = self.getModule(level, l_index)
        new_com = com[0:m.range[0]] + com[m.range[1]:]
        self._updateStructure(new_com)
    
    def getModule(self, level, index):
        module = self.getModules(level)[index]
        return module

    def getModules(self, level):
        modules = filter(lambda x: x.level == level, self.__modules)
        return list(modules)

    def addModule(self, new_module, text):
        new_module.setText(text, True)
        if (len(new_module.getChildren()) > 0):
            direct_modules = self.getModules(new_module.level + 1)
            for module in direct_modules:
                if (new_module.insideOf(module)):
                    module.addChild(new_module)
            
            self.__modules.extend(new_module.get_tree())
            def key(x):
                return x.level
            self.__modules.sort(key=key, reverse=True)

        elif (new_module.level == self.last_level):
            self.__modules.append(new_module)

        elif (new_module.level < self.last_level):
            direct_modules = self.getModules(new_module.level + 1)
            for i in range(len(direct_modules)):
                module = direct_modules[i]
                module.level_index = i
                if (module.insideOf(new_module)):
                    new_module.addChild(module)
            self.__modules = [*self.__modules, new_module]
        
    def getAllModules(self):
        return self.__modules
    def addModules(self, new_modules:list, common_text=""):
        for module in new_modules:
            self.addModule(module, common_text)
    def getModulesByText(self, text):
        coincidences = list(filter(lambda x: text in x.getText(), self.__modules))
        return coincidences if len(coincidences) > 0 else None

class NestedObj(MatrixObj):
    def __init__(self, range_, level, matrix):
        self.range = range_
        self.level = level
        self.level_index = 0
        self.__matrix = matrix
        self.__text = ""
        self.__children = []
        self.__parent = None
    def addChild(self, new_child):
        new_child.setParent(self)
        children = [*self.__children, new_child]
        def key (child):
            return child.range[0]
        
        children.sort(key=key)

        self.__children = children
    def getText(self):
        return self.__text
    def setText(self, string, is_common_string=False):
        s = self.range[0] if is_common_string else 0
        e = self.range[1] if is_common_string else len(string)
        new_text = string[s:e]
        if self.level == 0:
            new_text = "{" + new_text + "}"

        self.__text = new_text
        
        if (not is_common_string):
            self.__matrix.replaceModule(self, self.level, self.level_index)

    def getChildren(self):
        return self.__children
    def insideOf(self, module):
        starts_after = self.range[0] > module.range[0]
        ends_before = self.range[1] < module.range[1]
        return starts_after and ends_before
    def setParent(self, parent):
        if (self.getParent()):
            print("OVERWRITING\n", self.getParent(), "\nFOR", parent)
        self.__parent = parent

    def getParent(self):
        return self.__parent
    
    def get_tree(self):
        all_descendants = self.getChildren()
        for child in self.getChildren():
            if len(child.getChildren()) > 0:
                all_descendants.extend(child.get_tree())
        return all_descendants

    def __repr__(self) -> str:
        info = {
            "range": self.range,
            "level": self.level,
            "level_index": self.level_index,
            "text_content": self.__text,
            "childs": len(self.__children)

        }
        return str(info)

def searchAll(regex, string):
    matches = len(re.findall(regex, string))
    s = string + ""
    all_spans = []
    if matches == 0: return None
    
    for i in range(matches):
        sp = list(re.search(regex, s).span())
        if (len(all_spans) > 0):
            sp[0] += all_spans[-1][1]
            sp[1] += all_spans[-1][1] - 1
        
        all_spans.append(sp)
        s = s[sp[1]:]
    
    return all_spans

def changeStruct(old_structure, new_structure, string):
    old_structure = old_structure.split("REPLACE")
    new_structure = new_structure.split("PUT")

    if (len(old_structure) > len(new_structure)):
        print("BOTH STRUCTURES SHOULD HAVE THE SAME NUMBER OF -VAR PLACES")

    regex = ".+?".join(old_structure)

    matches = re.findall(regex, string)

    final_str = string + ""

    for match in matches:
        objective = match + ""
        sp = re.search(regex, final_str).span()
        for i in range(len(old_structure)):
            span = re.search(old_structure[i], objective).span()
            objective = objective[0:span[0]] + new_structure[i] + objective[span[1]:]

        final_str = final_str[:sp[0]] + objective + final_str[sp[1]:]

    return final_str

def put_structures (structs, matrix, l_l_op = None):
    for st in structs:
        modules = matrix.getModulesByText(st) if matrix.getModulesByText(st) else []
        if (l_l_op is None):
            l_l_op = modules[0].level if modules else matrix.last_level

        not_main = list(filter(lambda x: x.level == l_l_op, modules))
        for m in not_main:
            solved = changeStruct(*structs[st], m.getText())
            m.setText(solved)

def from_alt_to_txt (string):
    replacements = {
        ",": "",
        "\\": "",
        "text": "",
        "cdot": "*",
        "times": "×",
        "sum": "Σ",
        "nabla": "∇",
        "=&": "\n=",
        "~": "",
        "int": "∫",
        "ell": "ℓ",
        "sqrt": "√",
        "mathbf": "",
        ";": " ",
        r"begin{aligned}": "",
        r"end{aligned}": "",
        "mathrm": "",
        "displaystyle": "",
        "left": "",
        "right": ""
    }

    replacements.update(greek_letters)
    replacements.update(arrows)
    replacements.update(hats)

    for r in replacements:
        string = string.replace(r, replacements[r])

    matrix = MatrixObj(string)
    
    structures = {
        "frac": ["c?frac \{REPLACE\}\{REPLACE\}", "(PUT/PUT)"],
        "Σ _": ["Σ _\{REPLACE\}\^\{REPLACE\}", "Σ(PUT→PUT)"],
        "∫ _": ["∫ _\{REPLACE\}\^\{REPLACE\}", "∫(PUT→PUT)"],
        "over": ["\{REPLACE\} over \{REPLACE\}", "[(PUT)/(PUT)]"],
        "√ ": ["√ \{REPLACE\}", "√[PUT]"]
    }

    while_condition = [ 
        (matrix.getModulesByText(st) and matrix.getModulesByText(st)[0].level > 0) for st in structures
    ]
    count = 0

    while (any(while_condition) and count < 100):
        last_level_operations = [ 
            matrix.getModulesByText(st)[0] for st in structures if matrix.getModulesByText(st)
        ]

        limit = max([x.level for x in last_level_operations])

        erase_range = range(matrix.last_level - limit - 1)

        for i in erase_range:
            for j in range(len(matrix.getModules(matrix.last_level))):
                m = matrix.getModule(matrix.last_level, 0)
                m.setText(re.sub("[\{\}]", "", m.getText()))

        put_structures(structures, matrix, limit)

        if (count == 99):
            print("INFINITE WHILE LOOP")
            break

        count += 1
        while_condition = [ 
            (matrix.getModulesByText(st) and matrix.getModulesByText(st)[0].level > 0) for st in structures
        ]

    for i in range(matrix.last_level):
        for j in range(len(matrix.getModules(matrix.last_level))):
            m = matrix.getModule(matrix.last_level, 0)
            m.setText(re.sub("[\{\}]", "", m.getText()))

    adjustments = {
        "↔": " ↔ ",
        "=": " = ",
        "→": " → ",
        "×": " × ",
        "langle": "{",
        "rangle": "}"
    }

    adjusted = matrix.getCommon()[1:-1].replace(" ", "")

    for adj in adjustments:
        adjusted = adjusted.replace(adj, adjustments[adj])

    return adjusted
            
tests = [
    r"{1\,{\text{N}}=1\,{\frac {{\text{kg}}\cdot {\text{m}}}{{\text{s}}^{2}}}}",
    r"{\sum \mathbf {F} =\mathbf {0} \;\Leftrightarrow \;{\frac {\mathrm {d} \mathbf {v} }{\mathrm {d} t}}=\mathbf {0} .}",
    r"{\mathbf {p} =m\mathbf {v} }",
    r"{\mathbf {F} ={\frac {d\mathbf {p} }{dt}}}",
    r"{\mathbf {F} =\sum _{i=1}^{K}\mathbf {F} _{i}}",
    r"{ \mathbf {F} =m{\frac {d\mathbf {v} }{dt}}=m\mathbf {a} }",
    r"{\displaystyle \mathbf {F} =m{\frac {d\mathbf {v} }{dt}}-\mathbf {v} _{rel}{\frac {dm}{dt}}}",
    r"{\displaystyle \Delta \mathbf {p} =\mathbf {F} \Delta t}",
    r"{\displaystyle d\mathbf {p} =\mathbf {F} dt}",
    r"{\displaystyle \mathbf {I} =\int _{t_{1}}^{t_{2}}\mathbf {F} dt=\int _{\mathbf {p} _{1}}^{\mathbf {p} _{2}}d\mathbf {p} =\mathbf {p} _{2}-\mathbf {p} _{1}=\Delta \mathbf {p} }",
    r"{\displaystyle m\cdot a_{n}=T-mg\cdot \cos {\theta }}",
    r"{\displaystyle T=mg+{{m\cdot v^{2}} \over {\ell }}}",
    r"{\displaystyle {\mathbf {p}}={\cfrac {m{\mathbf {v}}}{\sqrt {1-{\frac {v^{2}}{c^{2}}}}}}}",
    r"{\displaystyle {\mathbf {F}}=m{\mathbf {a}}\left(1-{\frac {v^{2}}{c^{2}}}\right)^{-{\frac {3}{2}}}}",
    r"{\displaystyle {\mathbf {F}}={\frac {m{\mathbf {a}}}{(1-{\frac {v^{2}}{c^{2}}})^{\frac {1}{2}}}}+{\frac {m({\mathbf {v}}\cdot {\mathbf {a}}){\mathbf {v}}}{c^{2}(1-{\frac {v^{2}}{c^{2}}})^{\frac {3}{2}}}}}",
    r"{\displaystyle \mathbf {F} _{12}=q_{2}\mathbf {v} _{2}\times \mathbf {B} _{1}={\frac {\mu q_{2}q_{1}}{4\pi }}\ {\frac {\mathbf {v} _{2}\times (\mathbf {v} _{1}\times \mathbf {\hat {u}} _{12})}{d^{2}}}}",
    r"{\displaystyle {\begin{aligned}{\frac {d}{dt}}\langle p\rangle =&\int \Phi ^{*}V(x,t)\nabla \Phi ~dx^{3}-\int \Phi ^{*}(\nabla V(x,t))\Phi ~dx^{3}-\int \Phi ^{*}V(x,t)\nabla \Phi ~dx^{3}\\{}=&\;0-\int \Phi ^{*}(\nabla V(x,t))\Phi ~dx^{3}-0\\{}=&\;\langle -\nabla V(x,t)\rangle =\langle F\rangle ,\end{aligned}}}",
]

def run_tests(ts):
    for t in ts:
        result = from_alt_to_txt(t)
        print("FROM: " + t)
        print("TO: " + result + "\n")


#SEGUIR AGREGANDO MÁS SÍMBOLOS CONFORME SEA NECESARIO
#AGREGAR SOPORTE EN CASO DE QUE NO EXISTA UN "ALTTEXT" (usando BeautifulSoup)