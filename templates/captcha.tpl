{% macro captchas_begin(action) -%}
<form action="{{action}}" method="post" id="new">
<input type="hidden" name="hash" value="{{hash}}" />
<input type="hidden" name="reply" value="{{reply}}" />
{%- endmacro %}


{% macro captchas_body() -%}
    <fieldset class="captcha">
      <legend>
    <input type="radio" name="tcha" value="sum" id="sumtcha"/>
    <label for="sumtcha">Sumtcha</label>
      </legend>
      <p>
    Enter the sum of {{a}}, {{b}} and {{c}}:
    <input type="text" name="sumtcha" id="sumtcha" value="" size="3" tabindex="2" />
      </p>
    </fieldset>
    <fieldset class="captcha">
      <legend>
    <input type="radio" name="tcha" value="cat" checked="checked" id="cattcha"/>
    <label for="cattcha">Cattcha</label>
      </legend>
      <p>Select the feline animals to prove your fleshy nature:</p>
      <p>
    <input type="checkbox" name="cat" value="A" /><img src="/cat/A?{{hash}}" />
    <input type="checkbox" name="cat" value="B" /><img src="/cat/B?{{hash}}" /><br />
    <input type="checkbox" name="cat" value="C" /><img src="/cat/C?{{hash}}" />
    <input type="checkbox" name="cat" value="D" /><img src="/cat/D?{{hash}}" />
      </p>
    </fieldset>
{%- endmacro %}


{% macro captchas_end(submit) -%}
</p>
<input name="submit" id="submit" type="submit" tabindex="5" value="{{submit}}" style="position:absolute;margin-left:29em;" />


    </form>
<script src="/js/jquery-1.4.4.min.js" type="application/javascript" defer="defer"></script>
<script src="/js/captcha-form.js" type="application/javascript" defer="defer"></script>
{%- endmacro %}
