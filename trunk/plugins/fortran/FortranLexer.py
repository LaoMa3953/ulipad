#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
#  
#   Copyleft 2006 limodou
#  
#   Distributed under the terms of the GPL (GNU Public License)
#  
#   UliPad is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id$

from mixins.NCustomLexer import *
#from modules.ZestyParser import *
import re
    
class FortranLexer(CustomLexer):

    metaname = 'fortran'
    casesensitive = False

    def loadDefaultKeywords(self):
        return ('''admit allocatable allocate assign assignment at
backspace block
call case character close common complex contains continue cycle
data deallocate default dimension do double
else elseif elsewhere end enddo endfile endif endwhile entry equivalence execute exit external
forall format function
go goto guess
if implicit in inout inquire integer intent interface intrinsic
kind
logical loop
map module
namelist none nullify
only open operator optional otherwise out
parameter pointer private procedure program public
quit
read real record recursive remote result return rewind
save select sequence stop structure subroutine
target then to type
union until use
where while write''').split()

    def loadPreviewCode(self):
        return """
! Free Format
program main
write(*,*) "Hello" !This is also comment
write(*,*) &
"Hello"
wri&
&te(*,*) "Hello"
end
"""

    def initSyntaxItems(self):
        self.addSyntaxItem('r_default', 'Default',  STYLE_DEFAULT,  self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',   'Keyword',  STYLE_KEYWORD,  self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('comment',   'Comment',  STYLE_COMMENT,  self.STE_STYLE_COMMENT)
        self.addSyntaxItem('integer',   'Integer',  STYLE_INTEGER,  self.STE_STYLE_NUMBER)
        self.addSyntaxItem('string',    'String',   STYLE_STRING,   self.STE_STYLE_STRING)
                                                                    
        self.tokens = TokenList([
            (re.compile(r'^(!.*?)$', re.M), [(1, STYLE_COMMENT)]),
            (PATTERN_STRING, STYLE_STRING),
            (PATTERN_NUMBER, STYLE_INTEGER),
            (PATTERN_IDEN, self.is_keyword()),
        ])
