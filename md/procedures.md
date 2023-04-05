Title: DWARF Committee Procedures

# DWARF Debugging Information Format Committee Procedures

*May 16, 2021*

These are the processes and procedures used by the DWARF committee.


## Membership

Membership in the committee is by invitation only. The Chair or
Executive Committee may invite, at their discretion, individuals who
have been active on the `dwarf-discuss` mailing list or are actively
working on toolchains using DWARF and have demonstrated an interest in
the evolution of the DWARF standard. Members generally represent the
company they work for, but may also join as individual members
representing themselves.

Members are expected to participate in email discussions, meetings, and
editorial review of the standard, as described in the Member
Participation Agreement, and to follow the processes and procedures
described here.

Discussions within the committee take place on the `dwarf-workgroup`
mailing list, which is restricted to committee members. Members should
also subscribe to and follow discussions on the `dwarf-discuss` mailing
list, which is open to the public.

An up-to-date [list of members][members], along with their affiliations,
can be found on the [dwarfstd.org][home] website.


## Life of a Proposal

All proposed changes to the DWARF standard shall be submitted on the
[Public Comments][comment] page on the [dwarfstd.org][home] website.
Each proposal is tracked as a separate issue, and will appear on the
[Open Issues][issues] page until it has been resolved (either accepted
or rejected). Anyone, committee member or not, may submit an issue.

Proposals should be in plain English, and be self-contained. They may
refer to external websites (e.g., language standards) or to the DWARF
wiki pages for some background information, but should not rely on those
sources in order to be understood.

Proposals for enhancements to the standard should clearly indicate what
changes are being proposed, describing any background necessary for
understanding the issue and the rationale for the proposed change. Where
feasible, they should cite section and page numbers from the current
standard, along with proposed wording changes.

Proposals that are editorial in nature, that point out an ambiguity, or
that are requesting clarification, should always cite section and page
numbers, clearly indicating the issue with the current standard.

Proposals deemed to be incomplete are usually assigned to a committee
member, who may need to work with the original submitter to develop the
proposal as necessary for the committee to evaluate it.

Proposals may evolve over time. Early drafts may be somewhat conceptual;
this can be useful for setting the direction for a subsequent draft. A
final draft that is ready to be adopted should strive to identify all
places in the Standard that are being changed and include detailed
textual changes. Minor changes may be included at the time of adoption.

Occasionally, a proposal may be split into two or more separate issues,
or separate proposals may be combined into a single issue.


## Issue Champions

Every issue to be discussed in a committee meeting will have a
“champion” assigned, who will study the issue, work with the original
submitter if necessary, and be ready to present the proposal to the
committee at a regularly-scheduled meeting.

The Chair will typically go through the list of unassigned issues at the
beginning of a committee meeting, and ask for volunteers to champion
those issues. Ideally, each issue can be assigned to someone who has
expertise in the specific area, while distributing the workload fairly
evenly across the committee members. For issues submitted by committee
members, the Chair may look for a different member to act as
champion, in order to provide an alternate perspective or distribute
the workload.

The roles of a champion are:

1. Evaluating the proposal from the DWARF perspective, making sure that
the proposed changes are consistent with the DWARF philosophy and
existing features.

2. Rewriting the proposal as necessary to put it in the desired format,
with background, rationale, and specific wording changes, as
appropriate.

3. Presenting the issue to the committee for discussion once it has been
placed on the agenda.


## At the Meetings

Prior to each committee meeting, the Chair will send an announcement
with the meeting date and time, instructions for joining the meeting,
and an agenda listing what issues are scheduled to be discussed at that
meeting. Every member should read through the agenda, read the issues
listed there, and be prepared to discuss those issues at the meeting.
Any questions or suggestions related to an issue should be raised by
email prior to the meeting, if possible. Issue champions should be
prepared to present their issues at the meeting.

During the meeting, the Chair will go through the agenda, turning the
meeting over to the issue champions for discussion of each issue.
Discussion on an issue should remain focused on that issue, and the
Chair may direct that side discussions be saved for a future time, or
raised as a separate issue.

The Chair will ask for someone to serve as secretary during the meetings
and will work with that person to document the discussion and decisions
made during the meeting. The Chair will review the notes for accuracy,
and either the Chair or the secretary will send them to the committee
members after each meeting.

If, after discussion, an issue needs further revision, the champion
should update the text of the issue and send it to the Chair to update
the issue on the website (it’s common practice to cc the
`dwarf-workgroup` mailing list and include the word “UPDATE” and the
issue number in the subject line).


## Resolving an Issue

Once discussion has concluded on an issue, the Chair will seek a
decision by consensus. If there is no clear consensus, the Chair may
decide to schedule further discussion, or to call for a vote. If a vote
is called for, it will proceed as directed in the bylaws, with each
company or individual member receiving one vote.

An issue may be accepted as is, or with minor changes as specified in
the meeting, or it may be rejected. If minor changes are necessary, the
Chair may make those changes directly, or may request the champion to
provide a final update. If rejected, the Chair will update the issue
with the reasons for rejection.


## Updating the DWARF Standard

Once a change to the standard has been accepted by the committee, the
issue is passed to the Editor, who will update the working copy of the
standard document. If necessary, the Editor will communicate with the
champion to make and verify the changes.

The Editor is responsible for making any editorial changes necessary to
the final proposal, ensuring that the style is consistent with the rest
of the document. The Editor is also responsible for verifying that all
sections of the document that might be affected by the proposal have
been considered in the update.

The standard document is written in LaTeX, and stored in a git
repository hosted on [dwarfstd.org][home]. Members of the committee may
have read access to the repository so that they can see the current
state of the document, but only the Editor, or a member authorized by
the Editor, may commit changes to the main branch.


## Publishing a Revision of the DWARF Standard

From time to time, the committee will decide to publish a revision of
the standard.

In preparation for a new revision, the committee activity will focus on
closing open issues, and setting a target date for publication. After a
certain date, all new issues will be automatically deferred to a
subsequent version of the standard, and any current open issues that
cannot be resolved in time will also be deferred.

When all issues targeted for the new revision have been resolved and
updates sent to the Editor, the Editor will prepare a draft of the new
revision. The Chair will then call for a series of review meetings, and
the committee (or a designated subset) will conduct a thorough
page-by-page review of the document. Once the review is complete, the
Editor will prepare a final draft for approval by the committee. When
approved, the Chair will make the new draft standard available on the
[dwarfstd.org][home] website, and make a public announcement to call for
comments. After a suitable public review period, the committee will
review the comments received, update the document, and make the final
version available as the new DWARF standard.

[home]: index.html
[comment]: comment.html
[members]: members.html
[issues]: issues.html
