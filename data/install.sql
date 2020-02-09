--
-- Add new tab
--
INSERT INTO `core_form_tab` (`Tab_ID`, `form`, `title`, `subtitle`, `icon`, `counter`, `sort_id`, `filter_check`, `filter_value`) VALUES
('skeleton-skeleton', 'skeleton-single', 'Skeleton', 'Recent Skeleton', 'fas fa-skeleton', '', '1', '', '');

--
-- Add new partial
--
INSERT INTO `core_form_field` (`Field_ID`, `type`, `label`, `fieldkey`, `tab`, `form`, `class`, `url_view`, `url_list`, `show_widget_left`, `allow_clear`, `readonly`, `tbl_cached_name`, `tbl_class`, `tbl_permission`) VALUES
(NULL, 'partial', 'Skeleton', 'skeleton_skeleton', 'skeleton-skeleton', 'skeleton-single', 'col-md-12', '', '', '0', '1', '0', '', '', '');

--
-- create skeleton table
--
CREATE TABLE `skeleton_skeleton` (
  `Skeleton_ID` int(11) NOT NULL,
  `skeleton_idfs` int(11) NOT NULL,
  `comment` TEXT NOT NULL DEFAULT '',
  `created_by` int(11) NOT NULL,
  `created_date` datetime NOT NULL,
  `modified_by` int(11) NOT NULL,
  `modified_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `skeleton_skeleton`
  ADD PRIMARY KEY (`Skeleton_ID`);

ALTER TABLE `skeleton_skeleton`
  MODIFY `Skeleton_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- add skeleton form
--
INSERT INTO `core_form` (`form_key`, `label`, `entity_class`, `entity_tbl_class`) VALUES
('skeletonskeleton-single', 'Skeleton Skeleton', 'OnePlace\\Skeleton\\Skeleton\\Model\\Skeleton', 'OnePlace\\Skeleton\\Skeleton\\Model\\SkeletonTable');

--
-- add form tab
--
INSERT INTO `core_form_tab` (`Tab_ID`, `form`, `title`, `subtitle`, `icon`, `counter`, `sort_id`, `filter_check`, `filter_value`) VALUES
('skeleton-base', 'skeletonskeleton-single', 'Skeleton', 'Recent Skeleton', 'fas fa-skeleton', '', '1', '', '');

--
-- add address fields
--
INSERT INTO `core_form_field` (`Field_ID`, `type`, `label`, `fieldkey`, `tab`, `form`, `class`, `url_view`, `url_list`, `show_widget_left`, `allow_clear`, `readonly`, `tbl_cached_name`, `tbl_class`, `tbl_permission`) VALUES
(NULL, 'text', 'Comment', 'comment', 'skeleton-base', 'skeletonskeleton-single', 'col-md-6', '', '', '0', '1', '0', '', '', ''),
(NULL, 'hidden', 'Skeleton', 'skeleton_idfs', 'skeleton-base', 'skeletonskeleton-single', 'col-md-3', '', '/', '0', '1', '0', '', '', '');
