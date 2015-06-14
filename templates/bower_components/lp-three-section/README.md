# lp-three-section

A element to create three columns content with image and text/legend below that 
very common in vast majority of the landing pages.

Usage
=====
The class `title`, `highlight-[1,2,3]` and `text-highlight-[1,2,3]` are required
to compose this presentation.

In this sample I used images (sprited) sized width="145" height="144".

```
<lp-three-section minHeight="500" bgcolor="#F9F9F9" titlecolor="#979797">
      <span class="title">
      Art, Education & Social 
      </span>
      <div class="highlight-1">
        <!-- Above content commonly put img -->
        <img-sprite src="/images/sprite-call.png" width="145" height="144"></img-sprite>
      </div>
      <div class="highlight-2">
        <img-sprite src="/images/sprite-call.png"></img-sprite>
      </div>
      <div class="highlight-3">
        <img-sprite src="/images/sprite-call.png"></img-sprite>
      </div>
      <div class="text-highlight-1">
          <!-- label text placed below above content like images -->
          We're the art to approach and to ...
      </div>
      <div class="text-highlight-2">
          <!-- label text placed below above content like images -->
          Build personal identity. Insights to help... 
      </div>
      <div class="text-highlight-3">
          <!-- label text placed below above content like images -->
          Social for to create, share and learn from ... 
      </div>            
</lp-three-section>
```

Outcome
=======
![](https://github.com/horacioibrahim/landingpage-elements/blob/master/lp-three-section/outcome.png)
