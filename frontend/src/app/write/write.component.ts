import { Component, OnInit } from '@angular/core';
import { UserService } from '../models/user.service';
import { PlaneService } from '../models/plane.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-write',
  templateUrl: './write.component.html',
  styleUrls: ['./write.component.css']
})
export class WriteComponent implements OnInit {
  content = '';
  tag = '';

  constructor(private userService: UserService,
              private planeService: PlaneService,
              private router: Router) { }

  ngOnInit() {
    this.userService.getUser().then(user => {
      if (user.today_write_count <= 0) {
        alert('Sorry. You ran out of today\'s write count. Please wait until tomorrow!');
        this.router.navigate(['/my_page']);
      }
    });
  }

  validateInput(content: string, tag: string): boolean {
    if (content === '') {
      alert('Content is empty. Please fill in content!');
      return false;
    }

    if (tag === '') {
      alert('Tag is empty. Please fill in tag!');
      return false;
    }

    return true;
  }

  onClickCancelButton() {
    this.router.navigate(['/planes']);
  }

  onClickChangeSkyButton() {
    // TODO: Implement
    alert('Sorry. NOT IMPLEMENTED until now!');
  }

  onClickFoldButton() {
    // TODO: implement here
    if (!this.validateInput(this.content, this.tag)) {
      return;
    }

    this.planeService.foldNewPlane(this.content, this.tag).then(response => {
      if (response === 201) {
        this.router.navigate(['/planes']);
      } else {
        alert('An error occured. Please try again!');
      }
    });
  }
}
